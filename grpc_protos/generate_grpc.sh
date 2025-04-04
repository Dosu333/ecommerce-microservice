#!/bin/bash

PROTO_DIR=$(dirname "$0")
OUTPUT_DIR="$PROTO_DIR"

python -m grpc_tools.protoc \
  -I="$PROTO_DIR" \
  --python_out="$OUTPUT_DIR" \
  --grpc_python_out="$OUTPUT_DIR" \
  "$PROTO_DIR"/*.proto
