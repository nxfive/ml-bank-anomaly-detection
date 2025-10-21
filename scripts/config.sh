#!/bin/bash

echo "Creating alertmanager.yml from template..."
envsubst < /home/ubuntu/${APP_DIR}/alertmanager/alertmanager.yml.template > /home/ubuntu/${APP_DIR}/alertmanager/alertmanager.yml

echo "Creating filebeat.yml from template..."
envsubst < /home/ubuntu/${APP_DIR}/elk/filebeat/filebeat.yml.template > /home/ubuntu/${APP_DIR}/elk/filebeat/filebeat.yml

echo "Creating kibana.yml from template..."
envsubst < /home/ubuntu/${APP_DIR}/elk/kibana/kibana.yml.template > /home/ubuntu/${APP_DIR}/elk/kibana/kibana.yml

sudo chown root:root /home/ubuntu/${APP_DIR}/elk/filebeat/filebeat.yml
sudo chmod 600 /home/ubuntu/${APP_DIR}/elk/filebeat/filebeat.yml