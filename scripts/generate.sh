#!/bin/bash

# Generate new SDK using OpenAPI Generator
echo "Generating new SDK..."
poetry run openapi-generator-cli generate \
  -g python \
  -i https://api.perigon.io/v1/openapi/public-sdk \
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
