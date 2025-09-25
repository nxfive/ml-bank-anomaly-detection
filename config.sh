#!bin/bash

echo "Creating alertmanager.yml from template..."
envsubst < /home/ubuntu/${APP_DIR}/alertmanager/alertmanager.yml.template > /home/ubuntu/${APP_DIR}/alertmanager/alertmanager.yml

echo "Creating filebeat.yml from template..."
envsubst < /home/ubuntu/${APP_DIR}/elk/filebeat.yml.template > /home/ubuntu/${APP_DIR}/elk/filebeat.yml

sudo chown root:root /home/ubuntu/${APP_DIR}/elk/filebeat.yml
sudo chmod 644 /home/ubuntu/${APP_DIR}/elk/filebeat.yml