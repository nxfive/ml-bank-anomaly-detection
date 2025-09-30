#!/bin/bash
until curl -s -k -u ${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD} https://elasticsearch:9200 > /dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

KIBANA_TOKEN=$(curl -s -k -u elastic:${ELASTIC_PASSWORD} \
  -X POST "https://elasticsearch:9200/_security/service/elastic/kibana/credential/token" \
  -H "Content-Type: application/json" \
  | grep -oP '"value":"\K[^"]+')

export ELASTICSEARCH_USERNAME="elastic/kibana"
export ELASTICSEARCH_PASSWORD=$KIBANA_TOKEN

exec /usr/local/bin/kibana-docker "$@"
