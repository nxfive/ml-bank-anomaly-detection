#!/bin/bash
set -e

CERT_DIR="/home/ubuntu/${APP_DIR}/elk/certs"


mkdir -p "$CERT_DIR"
cd "$CERT_DIR"

openssl genrsa -out elasticsearch.key 2048

openssl req -new -x509 -key elasticsearch.key -out elasticsearch.crt -days 365 \
  -subj "/CN=elasticsearch"

cp elasticsearch.crt ca.crt

echo "Certificates generated in $CERT_DIR"
