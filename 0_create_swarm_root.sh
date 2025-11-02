#!/bin/bash
# Script to generate a password-protected CA root certificate.

set -e

echo "--- CA Certificate Generation ---"
read -p "Enter the Common Name for your new Certificate Authority (e.g., MyInternalCA): " COMMON_NAME

if [ -z "$COMMON_NAME" ]; then
    echo "Error: Common Name cannot be empty."
    exit 1
fi

# Define directory path
CA_DIR="./ca/${COMMON_NAME}"

# Create directory
mkdir -p "$CA_DIR"
echo "Created directory: $CA_DIR"

# Generate a password-protected private key for the CA [1, 2]
echo "Generating a 2048-bit RSA private key for the CA. You will be prompted for a password."
openssl genrsa -des3 -out "${CA_DIR}/ca.key" 2048

# Create a self-signed root certificate for the CA
echo "Creating the CA root certificate. You will be prompted for the CA key's password."
openssl req -new -x509 -days 3650 -key "${CA_DIR}/ca.key" -out "${CA_DIR}/ca.crt" -subj "/CN=${COMMON_NAME}"

echo ""
echo "--- Success! ---"
echo "CA private key created at: ${CA_DIR}/ca.key"
echo "CA root certificate created at: ${CA_DIR}/ca.crt"
echo "Keep your CA key and its password safe."
