FROM debian:latest

MAINTAINER Mark Ide Jr (https://www.mide.io)

# Install the needed packages
RUN apt-get update && \
    apt-get -y install wget python3 openjdk-7-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# Default JVM Options (Set default memory limit to 1G)
ENV JAVA_TOOL_OPTIONS "-Xmx1024M -Xms1024M"

# Add Minecraft user
RUN useradd minecraft --create-home --home-dir /minecraft --shell /bin/false
WORKDIR "/minecraft"

# Copy all the scripts into the container
COPY scripts/healthcheck.py /minecraft/healthcheck.py
COPY scripts/minecraft_rcon.py /minecraft/minecraft_rcon.py
COPY scripts/server_properties.py /minecraft/server_properties.py
COPY scripts/wrapper.py /minecraft/wrapper.py

# If running Vanilla Minecraft, only MINECRAFT_VERSION needs to be set. The
# default value of MINECRAFT_SERVER_DOWNLOAD_URL will use MINECRAFT_VERSION to
# find the correct Vanilla Minecraft server jar. If you want to run a
# non-vanilla Minecraft server (like Tekkit), you can set the environment
# variable MINECRAFT_SERVER_DOWNLOAD_URL and ignore MINECRAFT_VERSION.
ENV MINECRAFT_SERVER_DOWNLOAD_URL "https://s3.amazonaws.com/Minecraft.Download/versions/${MINECRAFT_VERSION}/minecraft_server.${MINECRAFT_VERSION}.jar"

RUN chmod +x /minecraft/healthcheck.py && \
    chmod +x /minecraft/wrapper.py && \
    chown minecraft -R /minecraft

# Switch to minecraft user, created above
USER minecraft

ENTRYPOINT ["/minecraft/wrapper.py"]

HEALTHCHECK CMD ["healthcheck.py"]
