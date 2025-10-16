#!/bin/bash
set -e

CERT_DIR="/home/ubuntu/${APP_DIR}/elk/certs"


mkdir -p "$CERT_DIR"
cd "$CERT_DIR"

openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -subj "/CN=cn-ca"

openssl genrsa -out elasticsearch.key 2048

openssl req -new -key elasticsearch.key -out elasticsearch.csr -subj "/CN=elasticsearch"

openssl x509 -req -in elasticsearch.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out elasticsearch.crt -days 365 -sha256

rm elasticsearch.csr

echo "Certificates generated in $CERT_DIR"
