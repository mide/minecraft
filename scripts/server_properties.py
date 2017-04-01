#!/usr/bin/python3

import configparser
import os

assert (os.path.isfile("/minecraft/server.properties")), "Expecting 'server.properties' to exist. Not found."

# Workaround since the server.properties doesn't have sections.
server_properties = configparser.ConfigParser()
with open('server.properties', 'r') as f:
    config_string = "[section_header]\n{}".format(f.read())
    server_properties.read_string(config_string)
server_properties = dict(server_properties["section_header"])

# Get Minecraft Port Number, Assert it's a valid port number.
minecraft_port_number = int(server_properties.get("server-port", 0))
assert (minecraft_port_number > 0 and minecraft_port_number <= 65534), "Expected 'server-port' to be set in server.properties. (And to be valid port)"

# Get RCON status, Assert it's set to true.
rcon_enable = (server_properties.get("enable-rcon", "").upper() == "TRUE")
assert rcon_enable, "Expected 'enable-rcon' to be set to 'true' in server.properties."

# Get RCON password, Assert it's not blank
rcon_password = server_properties.get("rcon.password", "")
assert (len(rcon_password) > 0), "Expected 'rcon.password' to be set in server.properties."

# Get RCON port, assert it's a valid port.
rcon_port = int(server_properties.get("rcon.port", 0))
assert (rcon_port > 0 and rcon_port <= 65534), "Expected 'rcon.port' to be set in server.properties. (And to be valid port)"
