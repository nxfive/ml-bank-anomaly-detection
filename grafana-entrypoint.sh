#!/bin/bash
while ! curl -s http://prometheus:9090/-/ready > /dev/null; do
  echo "Waiting for Prometheus..."
  sleep 2
done

exec /run.sh