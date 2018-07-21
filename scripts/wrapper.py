#!/usr/bin/python3

import json
import os
import signal
import subprocess
import sys
import urllib.request

import minecraft_rcon

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

# Minecraft now breaks their downloads up into two JSON API calls (instead of
# predictable URLs). The following function takes a version and a download_type
# (one of the strings 'client' or 'server'), and returns a URL that can be used
# to download the resource.
def get_minecraft_download_url(version, download_type):
    assert download_type in ['client', 'server'], "Invalid download_type. Expected client or server."
    with urllib.request.urlopen(MANIFEST_URL) as url:
        data = json.loads(url.read().decode())
    print("The latest Minecraft is {} (release) and {} (snapshot). You are requesting to download {}.".format(data['latest']['release'], data['latest']['snapshot'], version))

    desired_versions = list(filter(lambda v: v['id'] == version, data['versions']))
    assert len(desired_versions) != 0, "Couldn't find Minecraft Version {} in manifest file {}.".format(version, MANIFEST_URL)
    assert len(desired_versions) == 1, "Found more than one record published for version {} in manifest file {}.".format(version, MANIFEST_URL)

    version_manifest_url = desired_versions[0]['url']
    print("Found Version Metadata URL {} for version {}.".format(version_manifest_url, version))

    with urllib.request.urlopen(version_manifest_url) as url:
        data = json.loads(url.read().decode())

    download_url = data['downloads'][download_type]['url']
    print("Found final download URL for version {}. It is: {}".format(version, download_url))
    return download_url

def docker_stop_handler(signum, frame):
    print("SIGTERM signal detected. Stopping server.")
    minecraft_rcon.stop()

def download_minecraft():
    # Get MINECRAFT_VERSION from Environment Variable.
    minecraft_version = os.environ.get("MINECRAFT_VERSION", default=None)
    assert (minecraft_version is not None), "Expecting environment variable 'MINECRAFT_VERSION' to be set. It is not."
    minecraft_url =  get_minecraft_download_url(minecraft_version, 'server')

    print("Downloading Minecraft {} from URL: {}".format(minecraft_version, minecraft_url))
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
