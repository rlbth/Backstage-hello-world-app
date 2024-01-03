#!/bin/bash

# Define your Docker image name
IMAGE_NAME="hello-world-app"

# Pull the latest version of your image
docker pull $IMAGE_NAME:latest

# Stop the running container
docker stop $IMAGE_NAME-container

# Remove the stopped container
docker rm $IMAGE_NAME-container

# Run a new container with the latest image
docker run -d --name $IMAGE_NAME-container -p 5000:5000 $IMAGE_NAME:latest
