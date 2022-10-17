#!/bin/bash

curl http://localhost:8000 || \
echo "HEALTHCHECK FAILURE! RESTARTING!!" && \
bash -c 'kill -s 15 -1 && (sleep 10; kill -s 9 -1)'

