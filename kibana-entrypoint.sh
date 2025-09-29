#!/bin/bash
until curl -s -k -u ${ELASTIC_USERNAME}:${ELASTIC_PASSWORD} https://elasticsearch:9200; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

exec /usr/local/bin/kibana-docker "$@"
