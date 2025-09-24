#!bin/bash

envsubst < /etc/alertmanager/alertmanager.yml.template > /etc/alertmanager/alertmanager.yml

exec /bin/alertmanager "$@"