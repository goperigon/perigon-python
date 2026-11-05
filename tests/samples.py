"""Build the smallest values that satisfy generated Pydantic models.

The endpoint sweep uses these so each method can parse a fake response and
send a valid body without a recorded API payload.
"""

from __future__ import annotations

import inspect
import re
import types
from datetime import UTC, date, datetime
from enum import Enum
from typing import Annotated, Any, Union, get_args, get_origin
from uuid import UUID

from annotated_types import Ge, Gt, Le, Lt, MaxLen, MinLen
from pydantic import BaseModel

_ENUM_SET = re.compile(r"not in set\((\[.*?\])\)", re.DOTALL)
_QUOTED = re.compile(r"""["']([^"']+)["']""")

_MISSING = object()


def sample_model(
    model: type[BaseModel], seen: set[type[BaseModel]] | None = None
) -> BaseModel:
    """Return a valid instance with only required fields populated."""
    if seen is None:
        seen = set()
    if model in seen:
        return model.model_construct()
    seen.add(model)
    try:
        kwargs: dict[str, Any] = {}
        for name, field in model.model_fields.items():
            if not field.is_required():
                continue
            kwargs[name] = sample_value(
                field.annotation,
                metadata=list(field.metadata),
                model=model,
                field_name=name,
                seen=seen,
            )
        return model.model_validate(kwargs)
    finally:
        seen.discard(model)


def sample_json(model: type[BaseModel]) -> dict[str, Any]:
    """JSON object that ``model.model_validate`` accepts."""
    data: dict[str, Any] = sample_model(model).model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    model.model_validate(data)
    return data


def sample_argument(annotation: Any) -> Any:
    """Smallest value for one required method parameter."""
    return sample_value(annotation, seen=set())


def sample_value(
    annotation: Any,
    *,
    metadata: list[Any] | None = None,
    model: type[BaseModel] | None = None,
    field_name: str = "",
    seen: set[type[BaseModel]] | None = None,
    preferred: Any = _MISSING,
) -> Any:
    if seen is None:
        seen = set()
    if preferred is not _MISSING:
        return preferred

    annotation = _strip(annotation)
    allowed = _enum_values(model, field_name) if model is not None else None
    origin = get_origin(annotation)

    if origin in (list, set, frozenset):
        item_annotation = get_args(annotation)[0] if get_args(annotation) else str
        item_preferred: Any = _MISSING
        if allowed and _is_str(item_annotation):
            item_preferred = allowed[0]
        count = _min_len(metadata)
        return [
            sample_value(
                item_annotation,
                seen=seen,
                preferred=item_preferred,
            )
            for _ in range(count)
        ]

    if origin is dict:
        args = get_args(annotation)
        if _min_len(metadata) == 0:
            return {}
        key_annotation = args[0] if args else str
        value_annotation = args[1] if len(args) > 1 else str
        key = sample_value(key_annotation, seen=seen)
        return {str(key): sample_value(value_annotation, seen=seen)}

    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return sample_model(annotation, seen)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(iter(annotation))

    if _is_str(annotation):
        return _text(metadata, allowed[0] if allowed else None)

    if annotation is bool:
        return True
    if annotation is int:
        return _number(metadata, as_float=False)
    if annotation is float:
        return _number(metadata, as_float=True)
    if annotation is datetime:
        return datetime(2024, 1, 2, 3, 4, 5, tzinfo=UTC)
    if annotation is date:
        return date(2024, 1, 2)
    if annotation is UUID:
        return UUID("00000000-0000-0000-0000-000000000001")
    if annotation is bytes:
        return b"x"
    return "x"


def _strip(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is Annotated:
        return _strip(get_args(annotation)[0])
    if origin is Union or origin is types.UnionType:
        args = [item for item in get_args(annotation) if item is not type(None)]
        if len(args) == 1:
            return _strip(args[0])
        stripped = [_strip(item) for item in args]
        for preferred_type in (str, int, float, bool):
            if preferred_type in stripped:
                return preferred_type
        return stripped[0]
    return annotation


def _is_str(annotation: Any) -> bool:
    return _strip(annotation) is str


def _min_len(metadata: list[Any] | None) -> int:
    if not metadata:
        return 0
    for item in metadata:
        if isinstance(item, MinLen):
            return int(item.min_length)
    return 0


def _text(metadata: list[Any] | None, preferred: str | None) -> str:
    if preferred is not None:
        return preferred
    low = 1
    high: int | None = None
    for item in metadata or []:
        if isinstance(item, MinLen):
            low = max(low, int(item.min_length))
        if isinstance(item, MaxLen):
            limit = int(item.max_length)
            high = limit if high is None else min(high, limit)
    if high is not None and low > high:
        low = high
    if low <= 0:
        return "x" if high is None or high >= 1 else ""
    return "x" * low


def _as_float(value: Any) -> float:
    return float(value)


def _number(metadata: list[Any] | None, *, as_float: bool) -> int | float:
    low = 0.0
    high: float | None = None
    for item in metadata or []:
        if isinstance(item, Ge):
            low = max(low, _as_float(item.ge))
        elif isinstance(item, Gt):
            low = max(low, _as_float(item.gt) + 1)
        elif isinstance(item, Le):
            limit = _as_float(item.le)
            high = limit if high is None else min(high, limit)
        elif isinstance(item, Lt):
            limit = _as_float(item.lt) - 1
            high = limit if high is None else min(high, limit)
    chosen = low
    if chosen == 0 and (high is None or high >= 1):
        chosen = 1
    if high is not None and chosen > high:
        chosen = high
    if as_float:
        return float(chosen)
    return int(chosen)


def _enum_values(model: type[BaseModel], field_name: str) -> list[str] | None:
    decorators = model.__pydantic_decorators__.field_validators
    for decorator in decorators.values():
        if field_name not in decorator.info.fields:
            continue
        source = inspect.getsource(decorator.func)
        match = _ENUM_SET.search(source)
        if match is None:
            continue
        values = _QUOTED.findall(match.group(1))
        if values:
            return values
    return None
