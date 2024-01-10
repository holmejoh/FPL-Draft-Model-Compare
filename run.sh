#!/bin/bash

# Build Docker image from Dockerfile
docker build -t fpl-model-image -f Dockerfile .

# Run Docker container from the built image
docker run -d --name fpl-model-container fpl-model-image