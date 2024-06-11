#!/bin/bash

# Check if at least one argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <name1> <name2> ..."
    exit 1
fi

# Build Docker image from Dockerfile, passing names as arguments
docker build -t fpl-model-image -f Dockerfile --build-arg NAMES="$*" .

# Run Docker container from the built image
#docker run --name fpl-model-container fpl-model-image
docker run -d -v "$(pwd):/app" fpl-model-image

#docker logs -f fpl-model-container 2>&1
