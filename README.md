# Minecraft Docker Image

[![Docker](https://img.shields.io/docker/pulls/mide/minecraft.svg)](https://hub.docker.com/r/mide/minecraft/) [![Docker](https://img.shields.io/docker/stars/mide/minecraft.svg)](https://hub.docker.com/r/mide/minecraft/) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/mide/minecraft/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/mide/minecraft.svg)](https://github.com/mide/minecraft/issues)

## Motivation

**There are [many Minecraft Docker images](https://hub.docker.com/search/?isAutomated=0&isOfficial=0&page=1&pullCount=0&q=minecraft&starCount=0) already developed, why [develop another](https://xkcd.com/927/)?**

From what I was able to find, no Minecraft Docker image currently handles [signals](https://en.wikipedia.org/wiki/Unix_signal). That means when a `docker stop` command is issued, Docker will attempt to signal the process to gracefully quits, but the process ignores it. Docker then terminates the server without the Minecraft server saving the state, leaving the potential of corrupted data.

By writing a simple wrapper (`wrapper.py`), this image is able to process the `SIGTERM` signal that is sent by Docker during a `docker stop` command. That is then turned into an RCON call, which instructs the server to safely exit and close.

In order to keep simplicity, the container will be mounted to paths on the host disk. This will allow existing automation that manages things like `ops.txt` or `server.properties` to continue to work.

## Usage (Vanilla Minecraft)

```bash
# Copy configuraitons into Minecraft directory (If you have automation in
# place, run that here; that shouldn't need to change).
mkdir -p /srv/minecraft/
cp ~/my_server.properties /srv/minecraft/server.properties
echo "eula=true" > /srv/minecraft/eula.txt"

# Start Minecraft Server
docker run \
  -e MINECRAFT_VERISON=1.11.2 \
  -v /srv/minecraft/:/minecraft/:rw \
  --publish 25565:25565 \
  mide/minecraft:latest
```

## Options & Settings

### Required

|  Option | Expected Value | Location |
|---|---|---|
| `enable-rcon` | `true` | `server.properties`  |
| `rcon.password` | Your RCON Password  | `server.properties`  |
| `rcon.port` | Your RCON Port | `server.properties`  |
| `eula` | `true` | `eula.txt` |
| `MINECRAFT_VERSION` | Something like `1.11.2`| Environment Variable|

### Optional

|  Option | Description | Default Value | Location  |
|---|---|---|---|
|`JAVA_TOOL_OPTIONS` | JVM Settings, like heap size | `-Xmx1024M -Xms1024M` | Environment Variable|
|`broadcast-rcon-to-ops` | Announce RCON commands to Server Ops | `false` ??? TODO | `server.properties`|
