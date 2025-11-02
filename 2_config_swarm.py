#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">3.11"
# ///

import os
import stat

# --- Configuration Constants ---
BROKER_CERTS_DIR = "./broker_certs"
BROKER_CONFS_DIR = "./broker_confs"
ENCRYPTED_PORT = 18883
WEBSOCKET_PORT = 18443
MESSAGE_SIZE_LIMIT = 13370

# --- ACL File Content ---
ACL_CONTENT = """
# Default access for anonymous users
topic read pub/#
topic write pub/inbox

# Special access for user 'e'
user e
topic readwrite #
"""

def generate_configs():
    """
    Scans for broker certificates and generates mosquitto.conf files for a bridged mesh.
    """
    print("--- Mosquitto Configuration Generator ---")

    if not os.path.isdir(BROKER_CERTS_DIR):
        print(f"Error: Broker certificates directory '{BROKER_CERTS_DIR}' not found.")
        print("Please run the broker certificate generation script first.")
        return

    # Find all broker common names by listing subdirectories
    try:
        broker_names = sorted()
    except OSError as e:
        print(f"Error reading broker certificates directory: {e}")
        return

    if not broker_names:
        print("No broker certificates found. Nothing to generate.")
        return

    print(f"Found {len(broker_names)} brokers: {', '.join(broker_names)}")

    # Create the main output directory
    os.makedirs(BROKER_CONFS_DIR, exist_ok=True)

    # Generate config for each broker
    for current_broker in broker_names:
        print(f"Generating configuration for '{current_broker}'...")
        broker_conf_dir = os.path.join(BROKER_CONFS_DIR, current_broker)
        os.makedirs(broker_conf_dir, exist_ok=True)

        # --- 1. Generate acl.conf ---
        acl_file_path = os.path.join(broker_conf_dir, 'acl.conf')
        with open(acl_file_path, 'w') as f:
            f.write(ACL_CONTENT.strip())

        # --- 2. Generate mosquitto.conf ---
        conf_content =

        # General Settings
        conf_content.append("# --- General Settings ---")
        conf_content.append("persistence true")
        conf_content.append("persistence_location /mosquitto/data/")
        conf_content.append("allow_anonymous true")
        conf_content.append("acl_file /mosquitto/config/acl.conf")
        conf_content.append(f"message_size_limit {MESSAGE_SIZE_LIMIT}")
        conf_content.append("connection_messages true")
        conf_content.append("log_timestamp true")
        conf_content.append("tcp_nodelay true\n")


        # Listeners
        conf_content.append("# --- Listeners ---")
        # Secure listener for inter-broker bridge connections
        conf_content.append(f"listener {ENCRYPTED_PORT}")
        conf_content.append("protocol mqtt")
        conf_content.append("cafile /mosquitto/certs/ca.crt")
        conf_content.append(f"certfile /mosquitto/certs/{current_broker}.crt")
        conf_content.append(f"keyfile /mosquitto/certs/{current_broker}.key")
        conf_content.append("require_certificate true\n")

        # Secure WebSocket listener for clients [4, 5]
        conf_content.append(f"listener {WEBSOCKET_PORT}")
        conf_content.append("protocol websockets")
        conf_content.append("cafile /mosquitto/certs/ca.crt")
        conf_content.append(f"certfile /mosquitto/certs/{current_broker}.crt")
        conf_content.append(f"keyfile /mosquitto/certs/{current_broker}.key")
        # Client certificate is not required for this listener
        conf_content.append("require_certificate false\n")

        # Bridge Connections
        conf_content.append("# --- Bridge Connections ---")
        other_brokers = [name for name in broker_names if name!= current_broker]

        if not other_brokers:
            conf_content.append("# No other brokers to bridge to.")
        else:
            for other_broker in other_brokers:
                conf_content.append(f"connection {other_broker}")
                conf_content.append(f"address {other_broker}.mesh:{ENCRYPTED_PORT}")
                conf_content.append("topic # both 2")
                conf_content.append("try_private true")
                conf_content.append("bridge_cafile /mosquitto/certs/ca.crt")
                conf_content.append(f"bridge_certfile /mosquitto/certs/{current_broker}.crt")
                conf_content.append(f"bridge_keyfile /mosquitto/certs/{current_broker}.key")
                conf_content.append("") # Newline for separation

        # Write the config file
        conf_file_path = os.path.join(broker_conf_dir, 'mosquitto.conf')
        with open(conf_file_path, 'w') as f:
            f.write("\n".join(conf_content))

    print("\n--- Success! ---")
    print(f"All broker configurations have been generated in '{BROKER_CONFS_DIR}'.")

if __name__ == "__main__":
    generate_configs()

