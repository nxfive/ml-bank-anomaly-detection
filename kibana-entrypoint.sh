#!/bin/bash
until curl -s -k -u ${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD} https://elasticsearch:9200; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

exec /usr/local/bin/kibana-docker "$@"
