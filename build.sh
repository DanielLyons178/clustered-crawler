#!/bin/bash


if [ $# -eq 0 ] || [ $1 == 'core' ]; then
    echo "Building core"
    docker build . -f ./docker/scraper-core/Dockerfile -t scraper-core
fi

if [ $# -eq 0 ] || [ $1 == 'client' ]; then
    echo "Building client"
    docker build . -f ./docker/scraper-client/Dockerfile -t scraper-client-base
fi
if [ $# -eq 0 ] || [ $1 == 'sample' ] ; then
    echo "Building sample"
    docker build . -f ./docker/sample/Dockerfile -t scraper-sample
fi