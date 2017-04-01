#!/usr/bin/python3

import select
import socket
import struct
import sys

import server_properties

def stop():
    send("stop")

# NOTE: This has only been tested with "STOP" command. Your mileage may vary if
# you try to use this code outside this context.
def send(command):
    print("minecraft_rcon.py: found RCON Port: {}".format(server_properties.rcon_port))
    print("minecraft_rcon.py: found RCON Password: {}*******{}".format(server_properties.rcon_password[:1], server_properties.rcon_password[-1:]))
    print("minecraft_rcon.py: will inject the command '{}'.".format(command))

    null_padding = b'\x00\x00'
    rcon_password = server_properties.rcon_password.encode('utf8')
    command = command.encode('utf8')

    # Connect to RCON socket
    rcon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcon_socket.connect(('localhost', server_properties.rcon_port))

    # Send Login Packet, Receive response to process
    data_bytes = struct.pack('<ii', 0, 3) + rcon_password + null_padding
    length_bytes = struct.pack('<i', len(data_bytes))
    rcon_socket.send(length_bytes + data_bytes)
    response_length, = struct.unpack('<i', rcon_socket.recv(4))
    rcon_socket.recv(response_length)

    # Send STOP command Packet, Receive response to process
    data_bytes = struct.pack('<ii', 0, 2) + command + null_padding
    length_bytes = struct.pack('<i', len(data_bytes))
    rcon_socket.send(length_bytes + data_bytes)
    response_length, = struct.unpack('<i', rcon_socket.recv(4))
    rcon_socket.recv(response_length)

    # Close the Socket
    rcon_socket.close()
    rcon_socket = None
