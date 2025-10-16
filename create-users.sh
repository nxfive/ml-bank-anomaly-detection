#!/bin/bash
set -e

until curl -sk -u "elastic:${ELASTIC_PASSWORD}" ${ELASTIC_HOST} > /dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

echo "Creating role for Filebeat service..."
curl -sf -u "elastic:${ELASTIC_PASSWORD}" -X PUT "${ELASTIC_HOST}/_security/role/${ELASTIC_FILEBEAT_USER}_role" \
  --cacert /certs/ca.crt \
  -H 'Content-Type: application/json' -d '{
    "cluster": ["manage_index_templates", "monitor", "read_ilm", "manage_ilm"],
    "indices": [
      {
        "names": ["server-app-*"],
        "privileges": ["write","create_index","manage"]
      }
    ]
  }'
echo "Filebeat role created"

echo "Creating user for Filebeat service..."
curl -sf -u "elastic:${ELASTIC_PASSWORD}" -X POST "${ELASTIC_HOST}/_security/user/${ELASTIC_FILEBEAT_USER}" \
  --cacert /certs/ca.crt \
  -H "Content-Type: application/json" -d "{
    \"password\": \"${ELASTIC_FILEBEAT_PASS}\",
    \"roles\": [\"${ELASTIC_FILEBEAT_USER}_role\"]
  }"
echo "Filebeat user created"

echo "Updating password for Kibana service..."
curl -sf -u "elastic:${ELASTIC_PASSWORD}" -X POST "${ELASTIC_HOST}/_security/user/${ELASTIC_KIBANA_USER}/_password" \
  --cacert /certs/ca.crt \
  -H "Content-Type: application/json" -d "{
    \"password\": \"${ELASTIC_KIBANA_PASS}\"
  }"
echo "Kibana password updated"
