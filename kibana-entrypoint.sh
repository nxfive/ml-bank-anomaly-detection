#!/bin/bash
until curl -s -k -u ${ELASTIC_USERNAME}:${ELASTIC_PASSWORD} https://elasticsearch:9200 > /dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

KIBANA_TOKEN=$(curl -s -k -u ${ELASTIC_USERNAME}:${ELASTIC_PASSWORD} \
  -X POST "https://elasticsearch:9200/_security/service/kibana-system/credential/token" \
  -H "Content-Type: application/json" \
  | grep -oP '"value":"\K[^"]+')


cat > /usr/share/kibana/config/kibana.yml << EOF
    elasticsearch.hosts: ["https://elasticsearch:9200"]
    elasticsearch.username: "kibana-system"
    elasticsearch.password: "$KIBANA_TOKEN"
EOF

exec /usr/local/bin/kibana-docker "$@"
