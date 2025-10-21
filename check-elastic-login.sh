#!/bin/bash

set -e
set -o pipefail

echo "Waiting for Elasticsearch..."
until curl -v -u "${ELASTIC_USER}:${ELASTIC_PASS}" "${ELASTIC_HOST}" --cacert "${ELASTIC_CACERT}" > /dev/null; do
  echo "Unable to log in as user ${ELASTIC_USER}, retrying in 5s..."
  sleep 5
done

echo "Login successful - starting ${SERVICE}..."

unset ELASTIC_USER ELASTIC_PASS ELASTIC_HOST ELASTIC_CACERT KIBANA_ENCRYPTION_KEY KIBANA_REPORTING_KEY KIBANA_SECURITY_KEY

if [ "$SERVICE" = "kibana" ]; then
  exec /usr/local/bin/kibana-docker "$@"
elif [ "$SERVICE" = "filebeat" ]; then
  exec /usr/share/filebeat/filebeat -c /usr/share/filebeat/filebeat.yml -e
else
  echo "Unknown service. Exiting..."
  exit 1
fi