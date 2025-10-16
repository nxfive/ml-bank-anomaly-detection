#!/bin/bash

set -e

while ! curl -sf -u "${ELASTIC_USER}:${ELASTIC_PASS}" "${ELASTIC_HOST}" --cacert "${ELASTIC_CACERT}" > /dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 2
done

until curl -sf -u "${ELASTIC_USER}:${ELASTIC_PASS}" "${ELASTIC_HOST}" --cacert "${ELASTIC_CACERT}" > /dev/null; do
    echo "Unable to log in as user ${ELASTIC_USER}, waiting..."
    sleep 5
done
echo "Login successful - starting ${SERVICE}..."

if [ "$SERVICE" = "kibana" ]; then
  exec /usr/local/bin/kibana-docker "$@"
elif [ "$SERVICE" = "filebeat" ]; then
  exec /usr/share/filebeat/filebeat -e -strict.perms=false
else
  echo "Unknown service. Exiting... "
  exit 1
fi  