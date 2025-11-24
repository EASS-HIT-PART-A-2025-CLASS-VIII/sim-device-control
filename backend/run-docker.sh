#!/bin/bash

docker build -t sim-device-control .
docker run -p 8000:8000 sim-device-control
