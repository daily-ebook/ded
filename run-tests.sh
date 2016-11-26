#!/bin/bash
docker build \
    -f Dockerfile.test \
    -t daily-epub/ded-test .
docker run \
    --rm \
    daily-epub/ded-test