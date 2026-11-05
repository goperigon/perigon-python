#!/usr/bin/env python3
"""Pre-generation step for ``scripts/generate.sh``.

Downloads the remote Perigon OpenAPI spec and writes a local snapshot to
``.openapi-spec/spec.local.json`` for the generator.

Transformations applied before the generator runs:

1. Operation tags: an operation with no tags, or exactly one tag, is left
   unchanged. Untagged operations stay on the generator's ``DefaultApi``.
   When ``tags`` lists ``v1`` and at least one other tag, ``tags`` becomes
   ``["v1"]`` so the operation is emitted once. Several tags and no ``v1``
   stops generation.
2. Hidden properties: for each ``<Schema>: [<field>, ...]`` entry in
   ``scripts/spec-filters.json`` the matching property is removed from
   ``components.schemas.<Schema>`` and from its ``required`` list.
3. Excluded paths: every ``paths`` key that matches a listed glob is deleted
   so those operations never reach the generator. A pattern with no wildcards
   is an exact match. ``*`` covers one segment and ``**`` covers nested paths.
   Brace expansion is disabled, so ``{uuid}`` stays literal.
4. Article/NewsCluster cycle: ``NewsClusterArticle`` is ``Article`` without
   ``cluster``, and ``ArticleNewsCluster`` is ``NewsCluster`` without
   ``selectedArticles``. The nested refs point at those clones. Other
   ``Article`` and ``NewsCluster`` refs stay on the full schemas.
5. Orphan schemas: a fixed-point pass deletes any ``components.schemas`` entry
   with no remaining ``$ref`` from outside that schema. Hiding a property or
   dropping a path then also removes schemas that nothing else uses.

Usage:
    uv run python scripts/preprocess_spec.py
"""

from __future__ import annotations

import json
import sys
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from wcmatch import glob

SPEC_URL = "https://api.perigon.io/v1/openapi/public-sdk"
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PACKAGE_ROOT / "scripts" / "spec-filters.json"
OUTPUT_PATH = PACKAGE_ROOT / ".openapi-spec" / "spec.local.json"

# Match minimatch with nobrace, nocomment, and POSIX separators: `*` is one
# path segment, `**` crosses segments, and `{uuid}` stays literal.
_GLOB_FLAGS = glob.GLOBSTAR | glob.FORCEUNIX

USER_AGENT = "perigon-python-sdk-generator/1.0"

_V1_TAG = "v1"
_HTTP_METHODS = frozenset(
    {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
)


class SpecFiltersConfig(BaseModel):
    """Filters applied to the OpenAPI spec before SDK generation."""

    model_config = ConfigDict(populate_by_name=True)

    description: str = Field(alias="$description")
    hidden_fields: dict[str, list[str]] = Field(
        default_factory=dict,
        alias="hiddenFields",
    )
    excluded_paths: list[str] = Field(default_factory=list, alias="excludedPaths")


def fetch_spec(url: str) -> dict[str, Any]:
    print(f"Fetching OpenAPI spec from {url}")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Failed to fetch spec: HTTP {exc.code} {exc.reason}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Failed to fetch spec: response was not a JSON object")
    return payload


def load_spec_filters(path: Path) -> SpecFiltersConfig:
    return SpecFiltersConfig.model_validate_json(path.read_text(encoding="utf-8"))


def _schemas(spec: dict[str, Any]) -> dict[str, Any]:
    components = spec.get("components")
    if not isinstance(components, dict):
        return {}
    schemas = components.get("schemas")
    if not isinstance(schemas, dict):
        return {}
    return schemas


def _without(mapping: dict[str, Any], *keys: str) -> dict[str, Any]:
    excluded = set(keys)
    return {key: value for key, value in mapping.items() if key not in excluded}


def _with_schemas(spec: dict[str, Any], schemas: dict[str, Any]) -> dict[str, Any]:
    components = spec.get("components")
    if not isinstance(components, dict):
        raise RuntimeError("OpenAPI spec is missing components")
    return {**spec, "components": {**components, "schemas": schemas}}


def _schema_without_property(
    schema: dict[str, Any],
    field: str,
) -> dict[str, Any] | None:
    """Return ``schema`` without ``field``, or None when the field is absent."""
    properties = schema.get("properties")
    if not isinstance(properties, dict) or not properties.get(field):
        return None
    updated = {**schema, "properties": _without(properties, field)}
    required = schema.get("required")
    if not isinstance(required, list):
        return updated
    kept = [item for item in required if item != field]
    if kept:
        return {**updated, "required": kept}
    return _without(updated, "required")


def hide_properties(
    spec: dict[str, Any],
    hidden: dict[str, list[str]],
) -> tuple[dict[str, Any], int, list[str]]:
    """Remove hidden properties.

    Returns a new spec, the count applied, and entries skipped.
    Unchanged schema objects are reused. The input spec is not modified.
    """
    schemas = _schemas(spec)
    new_schemas = dict(schemas)
    applied = 0
    missing: list[str] = []

    for schema_name, fields in hidden.items():
        schema = new_schemas.get(schema_name)
        if not isinstance(schema, dict):
            missing.append(f"{schema_name} (schema not found)")
            continue
        for field in fields:
            updated = _schema_without_property(schema, field)
            if updated is None:
                missing.append(f"{schema_name}.{field} (property not found)")
                continue
            schema = updated
            applied += 1
            print(f"  Hid {schema_name}.{field}")
        new_schemas[schema_name] = schema

    if applied == 0:
        return spec, applied, missing
    return _with_schemas(spec, new_schemas), applied, missing


def path_matches(path: str, pattern: str) -> bool:
    return bool(glob.globmatch(path, pattern, flags=_GLOB_FLAGS))


def exclude_paths(
    spec: dict[str, Any],
    patterns: list[str],
) -> tuple[dict[str, Any], list[str], list[str]]:
    """Delete matching paths.

    Returns a new spec, removed paths, and patterns that matched nothing.
    Kept path items are reused. The input spec is not modified.
    """
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        return spec, [], list(patterns)

    unused = set(patterns)
    excluded: list[str] = []
    kept: dict[str, Any] = {}
    for path, path_item in paths.items():
        if not isinstance(path, str):
            kept[path] = path_item
            continue
        matched = False
        for pattern in patterns:
            if not path_matches(path, pattern):
                continue
            unused.discard(pattern)
            matched = True
        if not matched:
            kept[path] = path_item
            continue
        excluded.append(path)
        print(f"  Excluded path {path}")

    if not excluded:
        return spec, excluded, [pattern for pattern in patterns if pattern in unused]
    return (
        {**spec, "paths": kept},
        excluded,
        [pattern for pattern in patterns if pattern in unused],
    )


_ARTICLE = "Article"
_NEWS_CLUSTER = "NewsCluster"
_NEWS_CLUSTER_ARTICLE = "NewsClusterArticle"
_ARTICLE_NEWS_CLUSTER = "ArticleNewsCluster"

_NEWS_CLUSTER_ARTICLE_DESCRIPTION = (
    "Article embedded in a story cluster, without the parent cluster."
)
_ARTICLE_NEWS_CLUSTER_DESCRIPTION = (
    "Story cluster embedded on an article, without selected articles."
)


def _schema_ref(name: str) -> str:
    return f"#/components/schemas/{name}"


def _require_schema(schemas: dict[str, Any], name: str) -> dict[str, Any]:
    schema = schemas.get(name)
    if not isinstance(schema, dict):
        raise RuntimeError(
            f"Cannot split Article/NewsCluster cycle: schema {name} not found"
        )
    return schema


def _require_properties(schema: dict[str, Any], schema_name: str) -> dict[str, Any]:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: "
            f"{schema_name}.properties is missing"
        )
    return properties


def _drop_property(
    schema: dict[str, Any],
    schema_name: str,
    field: str,
) -> dict[str, Any]:
    properties = _require_properties(schema, schema_name)
    if field not in properties:
        raise RuntimeError(
            f"Cannot split Article/NewsCluster cycle: {schema_name}.{field} not found"
        )
    updated = {**schema, "properties": _without(properties, field)}
    required = schema.get("required")
    if not isinstance(required, list):
        return updated
    kept = [item for item in required if item != field]
    if kept:
        return {**updated, "required": kept}
    return _without(updated, "required")


def _retarget_all_of_ref(
    property_schema: dict[str, Any],
    expected: str,
    replacement: str,
) -> dict[str, Any]:
    all_of = property_schema.get("allOf")
    if not isinstance(all_of, list):
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: Article.cluster.allOf is missing"
        )
    updated_entries: list[Any] = []
    found = False
    for entry in all_of:
        if not isinstance(entry, dict) or entry.get("$ref") != expected:
            updated_entries.append(entry)
            continue
        updated_entries.append({**entry, "$ref": replacement})
        found = True
    if not found:
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: "
            "Article.cluster.allOf does not reference NewsCluster"
        )
    return {**property_schema, "allOf": updated_entries}


def _retarget_items_ref(
    property_schema: dict[str, Any],
    expected: str,
    replacement: str,
) -> dict[str, Any]:
    items = property_schema.get("items")
    if not isinstance(items, dict) or items.get("$ref") != expected:
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: "
            "NewsCluster.selectedArticles.items does not reference Article"
        )
    return {**property_schema, "items": {**items, "$ref": replacement}}


def split_article_cluster_cycle(spec: dict[str, Any]) -> dict[str, Any]:
    """Replace the Article ↔ NewsCluster cycle with two non-cyclic slices.

    ``NewsClusterArticle`` is ``Article`` without ``cluster``.
    ``ArticleNewsCluster`` is ``NewsCluster`` without ``selectedArticles``.
    Only the nested refs are retargeted; top-level payloads keep the full schemas.
    Returns a new spec. The input spec is not modified.
    """
    schemas = _schemas(spec)
    if not schemas:
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: components.schemas is missing"
        )

    article = _require_schema(schemas, _ARTICLE)
    cluster = _require_schema(schemas, _NEWS_CLUSTER)
    article_properties = _require_properties(article, _ARTICLE)
    cluster_properties = _require_properties(cluster, _NEWS_CLUSTER)
    cluster_property = article_properties.get("cluster")
    selected_articles = cluster_properties.get("selectedArticles")
    if not isinstance(cluster_property, dict):
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: Article.cluster is missing"
        )
    if not isinstance(selected_articles, dict):
        raise RuntimeError(
            "Cannot split Article/NewsCluster cycle: "
            "NewsCluster.selectedArticles is missing"
        )

    news_cluster_article = {
        **_drop_property(article, _ARTICLE, "cluster"),
        "description": _NEWS_CLUSTER_ARTICLE_DESCRIPTION,
    }
    article_news_cluster = {
        **_drop_property(cluster, _NEWS_CLUSTER, "selectedArticles"),
        "description": _ARTICLE_NEWS_CLUSTER_DESCRIPTION,
    }
    article_ref = _schema_ref(_ARTICLE)
    cluster_ref = _schema_ref(_NEWS_CLUSTER)
    new_article = {
        **article,
        "properties": {
            **article_properties,
            "cluster": _retarget_all_of_ref(
                cluster_property,
                cluster_ref,
                _schema_ref(_ARTICLE_NEWS_CLUSTER),
            ),
        },
    }
    new_cluster = {
        **cluster,
        "properties": {
            **cluster_properties,
            "selectedArticles": _retarget_items_ref(
                selected_articles,
                article_ref,
                _schema_ref(_NEWS_CLUSTER_ARTICLE),
            ),
        },
    }
    print(
        "  Split Article/NewsCluster cycle into "
        f"{_NEWS_CLUSTER_ARTICLE} and {_ARTICLE_NEWS_CLUSTER}"
    )
    return _with_schemas(
        spec,
        {
            **schemas,
            _ARTICLE: new_article,
            _NEWS_CLUSTER: new_cluster,
            _NEWS_CLUSTER_ARTICLE: news_cluster_article,
            _ARTICLE_NEWS_CLUSTER: article_news_cluster,
        },
    )


def collect_refs(node: object, acc: set[str]) -> None:
    """Collect every ``$ref`` string in ``node``."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                acc.add(value)
            else:
                collect_refs(value, acc)
    elif isinstance(node, list):
        for item in node:
            collect_refs(item, acc)


def prune_orphan_schemas(spec: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Delete schemas with no ``$ref`` from outside themselves.

    A schema that only references itself is removed. Schemas that reference
    each other stay, matching the TypeScript preprocessor: a ref counts when
    it comes from any other node. Returns a new spec and the pruned names.
    The input spec is not modified.
    """
    components = spec.get("components")
    if not isinstance(components, dict):
        return spec, []
    original_schemas = components.get("schemas")
    if not isinstance(original_schemas, dict) or not original_schemas:
        return spec, []

    schemas = dict(original_schemas)
    pruned: list[str] = []
    while True:
        view = {**spec, "components": {**components, "schemas": schemas}}
        all_refs: set[str] = set()
        collect_refs(view, all_refs)

        removed_this_pass = 0
        for name in list(schemas):
            target = f"#/components/schemas/{name}"
            if target in all_refs:
                saved = schemas[name]
                del schemas[name]
                refs_without_self: set[str] = set()
                collect_refs(
                    {**spec, "components": {**components, "schemas": schemas}},
                    refs_without_self,
                )
                if target not in refs_without_self:
                    pruned.append(name)
                    print(f"  Pruned orphan schema {name}")
                    removed_this_pass += 1
                    continue
                schemas[name] = saved
            else:
                del schemas[name]
                pruned.append(name)
                print(f"  Pruned orphan schema {name}")
                removed_this_pass += 1

        if removed_this_pass == 0:
            break

    if not pruned:
        return spec, pruned
    return _with_schemas(spec, schemas), pruned


def prefer_v1_tag(spec: dict[str, Any]) -> dict[str, Any]:
    """Keep a single ``v1`` tag when an operation lists several tags.

    An operation with no tags, or exactly one tag, is left unchanged. The
    generator assigns untagged operations to ``DefaultApi``.

    When ``tags`` contains ``v1`` and at least one other tag, ``tags`` is
    replaced with ``["v1"]``. When it contains several tags and ``v1`` is
    not among them, generation stops. The input spec is not modified.
    """
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        return spec

    new_paths: dict[str, Any] = {}
    changed = False
    for path, path_item in paths.items():
        if not isinstance(path, str) or not isinstance(path_item, dict):
            new_paths[path] = path_item
            continue

        new_item: dict[str, Any] | None = None
        for method, operation in path_item.items():
            if (
                not isinstance(method, str)
                or method.lower() not in _HTTP_METHODS
                or not isinstance(operation, dict)
            ):
                continue
            tags = operation.get("tags")
            if not isinstance(tags, list) or len(tags) <= 1:
                continue
            label = f"{method.upper()} {path}"
            operation_id = operation.get("operationId")
            if isinstance(operation_id, str) and operation_id:
                label = f"{label} ({operation_id})"
            if _V1_TAG not in tags:
                raise RuntimeError(
                    "Operation has multiple tags and none of them is 'v1': "
                    f"{label} tags={tags}"
                )
            if new_item is None:
                new_item = dict(path_item)
            new_item[method] = {**operation, "tags": [_V1_TAG]}
            changed = True
            print(f"  Kept v1 tag for {label} (was {tags})")

        new_paths[path] = path_item if new_item is None else new_item

    if not changed:
        return spec
    return {**spec, "paths": new_paths}


def _warn(title: str, items: list[str]) -> None:
    print(title, file=sys.stderr)
    for item in items:
        print(f"    - {item}", file=sys.stderr)


def main() -> None:
    config = load_spec_filters(CONFIG_PATH)
    hidden_entries = [
        f"{schema_name}.{field}"
        for schema_name, fields in config.hidden_fields.items()
        for field in fields
    ]
    print("Loaded spec filters from scripts/spec-filters.json")
    hidden_summary = f"  {len(hidden_entries)} hidden field(s)"
    if hidden_entries:
        hidden_summary += f": {', '.join(hidden_entries)}"
    print(hidden_summary)
    path_summary = f"  {len(config.excluded_paths)} excluded path pattern(s)"
    if config.excluded_paths:
        path_summary += f": {', '.join(config.excluded_paths)}"
    print(path_summary)

    spec = fetch_spec(SPEC_URL)
    spec = prefer_v1_tag(spec)

    spec, applied, missing = hide_properties(spec, config.hidden_fields)
    if missing:
        _warn(
            f"Skipped {len(missing)} hidden-field entry/entries (not present in spec):",
            missing,
        )

    spec, excluded, unused = exclude_paths(spec, config.excluded_paths)
    if unused:
        _warn(
            f"Skipped {len(unused)} excluded-path pattern(s) (no matching paths):",
            unused,
        )

    spec = split_article_cluster_cycle(spec)

    spec, pruned = prune_orphan_schemas(spec)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote preprocessed spec to {OUTPUT_PATH} "
        f"({applied} field(s) hidden, {len(excluded)} path(s) excluded, "
        f"{len(pruned)} orphan schema(s) pruned"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
