#!/bin/bash

docker build -t sim-device-backend .
docker run -p 8000:8000 sim-device-backend
