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

# docker buildx create --use
# docker buildx build --platform linux/amd64 -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

# echo "Successfully built $DOCKER_USERNAME/$IMAGE_NAME:$TAG"

docker buildx inspect mybuilder >/dev/null 2>&1 || docker buildx create --name mybuilder
docker buildx use mybuilder
docker buildx build --platform linux/amd64 \
--build-arg BUILDPLATFORM=linux/amd64 \
--build-arg TARGETPLATFORM=linux/amd64 \
 -t $DOCKER_PATH/$DOCKER_REGISTRY:$TAG \
 --push .
docker buildx rm mybuilder

echo "Successfully built and pushed $DOCKER_PATH/$DOCKER_REGISTRY:$TAG"

# # Push to aliyun registry
# docker tag $DOCKER_USERNAME/$IMAGE_NAME:$TAG $DOCKER_PATH/$DOCKER_REGISTRY:$TAG

# docker push $DOCKER_PATH/$DOCKER_REGISTRY:$TAG

# echo "Successfully built and pushed $DOCKER_PATH/$DOCKER_REGISTRY:$TAG"