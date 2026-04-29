#!/bin/bash
set -euo pipefail

# Preprocess the OpenAPI spec to strip fields that should not appear in the
# public Python SDK (e.g. Article.vectors which is reserved for specific
# customers). The helper writes the modified spec to disk and prints its path.
echo "Preprocessing OpenAPI spec..."
SPEC_PATH="$(poetry run python scripts/preprocess_spec.py)"

# Generate new SDK using OpenAPI Generator
echo "Generating new SDK from $SPEC_PATH..."
poetry run openapi-generator-cli generate \
  -g python \
  -i "$SPEC_PATH" \
  -o ./ \
  -t templates \
  -c python.config.json \
  --package-name perigon \
  --global-property=apiDocs=false,modelDocs=false

# Format the generated code
echo "Formatting generated code with isort..."
poetry run isort ./

echo "Formatting generated code with black..."
poetry run black ./

echo "SDK generation and formatting complete!"
