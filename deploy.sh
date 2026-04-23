#!/bin/bash

set -e

APP_NAME="gcloud"
REPO_DIR="/home/ubuntu/app/gcloudproject"
IMAGE_NAME="gcloud-image"
CONTAINER_NAME="gcloud-container"
PORT=3000   # change to your app port

echo "=== Pulling latest code ==="
cd $REPO_DIR
git fetch --all
git reset --hard origin/main

echo "=== Building Docker image ==="
docker build -t $IMAGE_NAME .

echo "=== Stopping old container (if exists) ==="
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    docker stop $CONTAINER_NAME
fi

echo "=== Removing old container (if exists) ==="
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker rm $CONTAINER_NAME
fi

echo "=== Running new container ==="
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:$PORT \
  --restart always \
  $IMAGE_NAME

echo "=== Cleaning up old images ==="
docker image prune -f

echo "=== Deployment complete ==="
