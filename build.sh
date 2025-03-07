#!/bin/bash
set -e

# Load environment variables
source .env

# Docker Hub username and repository name
# Verify required environment variables
if [ -z "$DOCKER_USERNAME" ]; then
    echo "Error: DOCKER_USERNAME is not set in .env file"
    exit 1
fi

if [ -z "$DOCKER_REGISTRY" ]; then
    echo "Error: DOCKER_REGISTRY is not set in .env file"
    exit 1
fi
IMAGE_NAME="megatrip"
TAG="latest"

# Login to Docker Hub (first time only)
# docker login

# Build the image
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

# Push to aliyun registry
docker tag $DOCKER_USERNAME/$IMAGE_NAME:$TAG $DOCKER_PATH/$DOCKER_REGISTRY:$TAG

docker push $DOCKER_PATH/$DOCKER_REGISTRY:$TAG

echo "Successfully built and pushed $DOCKER_PATH/$DOCKER_REGISTRY:$TAG"