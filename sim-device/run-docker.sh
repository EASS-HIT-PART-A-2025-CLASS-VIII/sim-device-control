#!/bin/bash

docker build -t mqtt-device .
docker run --network host mqtt-device

