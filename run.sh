#!/bin/bash

# Parse command-line arguments
ARGS=()

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--tool) ARGS+=("--tool" "$2"); shift ;;
        -p|--position) ARGS+=("--position" "$2"); shift ;;
        -n|--names) ARGS+=("--names" "$2"); shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Build the Docker image
docker build -t fpl-draft-model .

# Run the Docker container with the provided arguments
docker run --rm fpl-draft-model "${ARGS[@]}"
