#!bin/bash

echo "Creating alertmanager.yml from template..."
envsubst < /home/ubuntu/${APP_DIR}/alertmanager/alertmanager.yml.template > /home/ubuntu/${APP_DIR}/alertmanager/alertmanager.yml