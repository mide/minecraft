#!/usr/bin/python3

import sys
import socket

import server_properties

def minecraft_port_is_open():
    port_number = server_properties.rcon_port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(('localhost', port_number)) == 0

# If we're calling on this script directly, exit with
# the return code signifying the status.
if __name__ == "__main__":
    if minecraft_port_is_open():
        sys.exit(0) # Pass Healthcheck
    else:
        sys.exit(1) # Fail Healthcheck
