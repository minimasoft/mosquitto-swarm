#!/bin/bash
# Script to generate a certificate for a Mosquitto broker, signed by the CA.

set -e

echo "--- Broker Certificate Generation ---"

# Get Broker Common Name
read -p "Enter the Common Name for the broker (e.g., broker1): " BROKER_CN
if; then
    echo "Error: Broker Common Name cannot be empty."
    exit 1
fi

# Get CA Common Name
read -p "Enter the Common Name of the CA that will sign this certificate: " CA_CN
if [ -z "$CA_CN" ]; then
    echo "Error: CA Common Name cannot be empty."
    exit 1
fi

# Define paths
CA_DIR="./ca/${CA_CN}"
BROKER_DIR="./broker_certs/${BROKER_CN}"
CA_KEY="${CA_DIR}/ca.key"
CA_CERT="${CA_DIR}/ca.crt"

# Check if CA files exist
if ||; then
    echo "Error: CA key or certificate not found at ${CA_DIR}."
    echo "Please run the CA generation script first."
    exit 1
fi

# Create broker directory
mkdir -p "$BROKER_DIR"
echo "Created directory: $BROKER_DIR"

# Generate a private key for the broker (not password protected) [3]
echo "Generating a 2048-bit RSA private key for the broker..."
openssl genrsa -out "${BROKER_DIR}/${BROKER_CN}.key" 2048

# Generate a certificate signing request (CSR) for the broker
echo "Creating a Certificate Signing Request (CSR)..."
openssl req -new -key "${BROKER_DIR}/${BROKER_CN}.key" -out "${BROKER_DIR}/${BROKER_CN}.csr" -subj "/CN=${BROKER_CN}"

# Sign the broker's CSR with the CA [2]
echo "Signing the broker certificate with the CA. You will be prompted for the CA key's password."
openssl x509 -req -in "${BROKER_DIR}/${BROKER_CN}.csr" \
    -CA "$CA_CERT" \
    -CAkey "$CA_KEY" \
    -CAcreateserial \
    -out "${BROKER_DIR}/${BROKER_CN}.crt" \
    -days 1826

# Copy the CA certificate to the broker's directory
cp "$CA_CERT" "${BROKER_DIR}/ca.crt"

# Clean up the CSR
rm "${BROKER_DIR}/${BROKER_CN}.csr"
# Move the.srl file to the CA directory for subsequent signings
mv./*.srl "${CA_DIR}/" 2>/dev/null |

| true


echo ""
echo "--- Success! ---"
echo "Broker certificate files created in: ${BROKER_DIR}"
echo " - ${BROKER_CN}.key (Broker Private Key)"
echo " - ${BROKER_CN}.crt (Broker Certificate)"
echo " - ca.crt (CA Certificate)"
