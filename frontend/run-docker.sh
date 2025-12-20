#!/bin/bash

docker build -t sim-device-frontend .
docker run -p 5173:5173 sim-device-frontend