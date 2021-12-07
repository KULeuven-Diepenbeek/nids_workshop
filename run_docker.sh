#!/bin/bash

docker build ./dockerfile --tag esns_nids_workshop
docker run -p 8888:8888 -v $(pwd):/home/jovyan/app esns_nids_workshop:latest
