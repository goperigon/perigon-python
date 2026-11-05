#!/usr/bin/env bash
set -euo pipefail

# 1. Download the remote Perigon OpenAPI spec and preprocess it: keep a single
#    v1 tag when an operation lists several, hidden fields and excluded paths
#    from scripts/spec-filters.json, the Article/NewsCluster cycle split, and
#    orphan-schema pruning. The snapshot is written to
#    .openapi-spec/spec.local.json.
uv run python scripts/preprocess_spec.py

# 2. Generate the Python SDK from that snapshot.
#    -c openapi-config.yaml
#         package name, httpx library, src layout, and the other generator options
#    -g python
#    --global-property apiDocs=false,modelDocs=false,apiTests=false,modelTests=false
#         skip generated docs and tests
#    -i .openapi-spec/spec.local.json
#    -t templates
#         custom Mustache templates
#
uv run openapi-generator-cli generate \
  -c openapi-config.yaml \
  -g python \
  --global-property apiDocs=false,modelDocs=false,apiTests=false,modelTests=false \
  -i .openapi-spec/spec.local.json \
  -t templates

# 3. Lint and format the generated package.
uv run ruff check --fix
uv run ruff format

# 4. Typecheck, then run the test suite.
uv run mypy
uv run pytest
