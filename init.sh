#!/bin/bash
set -e

until curl -s -k -u elastic:${ELASTIC_PASSWORD} ${ELASTIC_HOST} > /dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

curl -s -k -u elastic:${ELASTIC_PASSWORD} -X PUT "${ELASTIC_HOST}/_security/role/${SERVICE}_role" \
--cacert /usr/share/elasticsearch/config/certs/ca.crt \
-H 'Content-Type: application/json' -d '{
  "cluster": ["manage_index_templates", "monitor", "read_ilm"],
  "indices": [
    {
      "names": ["server-app-*"],
      "privileges": ["write","create_index","manage"]
    }
  ]
}'

curl -s -k -u elastic:${ELASTIC_PASSWORD} -X POST "${ELASTIC_HOST}/_security/user/${SERVICE}" \
--cacert /usr/share/elasticsearch/config/certs/ca.crt \
-H "Content-Type: application/json" -d "{
  \"password\": \"${ELASTIC_SERVICE_PASS}\",
  \"roles\": [\"filebeat_writer_role\"],
  \"full_name\": \"Filebeat Writer\"
}"

case "$SERVICE" in
  filebeat)
    exec /usr/share/filebeat/filebeat "$@"
    ;;
  kibana)
    exec /usr/local/bin/kibana-docker "$@"
    ;;
  *)
    echo "Unknown service: $SERVICE"
    exit 1
    ;;
esac