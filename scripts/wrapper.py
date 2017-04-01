#!/usr/bin/python3

import time
import signal
import sys
import subprocess
import os

import minecraft_rcon

def docker_stop_handler(signum, frame):
    print("SIGTERM signal detected. Stopping server.")
    minecraft_rcon.stop()

def download_minecraft():
    # Get MINECRAFT_SERVER_DOWNLOAD_URL from Environment Variable.
    minecraft_url = os.environ.get("MINECRAFT_SERVER_DOWNLOAD_URL", default=None)
    assert (minecraft_url is not None), "Expecting environment variable 'MINECRAFT_SERVER_DOWNLOAD_URL' to be set. It is not."
    assert (minecraft_url != "https://s3.amazonaws.com/Minecraft.Download/versions//minecraft_server..jar"), "It appears you didn't set MINECRAFT_VERSION, so I wasn't able to determine the server URL. Please specify either MINECRAFT_VERSION (for vanilla) or MINECRAFT_SERVER_DOWNLOAD_URL (for non-vanilla)."

    print("Downloading Minecraft from URL: {}".format(minecraft_url))
    subprocess.Popen(["wget", "-O", "minecraft_server.jar", minecraft_url]).wait()

def run_minecraft():
    subprocess.Popen(["java", "-jar", "minecraft_server.jar", "nogui"]).wait()

if __name__ == "__main__":
    # Associate SIGTERM with the custom handler
    signal.signal(signal.SIGTERM, docker_stop_handler)

    download_minecraft()
    try:
        run_minecraft()
    except Exception as e:
        # Something unexpected happened. Try to gracefully quit.
        print(e)
        minecraft_rcon.stop()
        sys.exit(1)

    sys.exit(0)
