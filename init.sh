#!/bin/bash
set -e

until curl -s -k -u elastic:${ELASTIC_PASSWORD} ${ELASTIC_HOST} > /dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

curl -s -k -u elastic:${ELASTIC_PASSWORD} -X PUT "${ELASTIC_HOST}/_security/role/filebeat_writer_role" \
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

curl -s -k -u elastic:${ELASTIC_PASSWORD} -X POST "${ELASTIC_HOST}/_security/user/filebeat_writer" \
--cacert /usr/share/elasticsearch/config/certs/ca.crt \
-H "Content-Type: application/json" -d "{
  \"password\": \"${ELASTIC_FILEBEAT_PASS}\",
  \"roles\": [\"filebeat_writer_role\"],
  \"full_name\": \"Filebeat Writer\"
}"

exec /usr/share/filebeat/filebeat "$@"