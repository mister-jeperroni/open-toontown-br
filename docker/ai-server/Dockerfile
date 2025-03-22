FROM ubuntu:20.04

# Prevent tzdata questions during install
ENV DEBIAN_FRONTEND=noninteractive

# Add repository for newer packages
RUN apt-get update && apt-get install -y software-properties-common \
    build-essential \
    pkg-config \
    fakeroot \ 
    python3-dev \
    python3-pip \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    zlib1g-dev \
    libssl-dev \
    libx11-dev \
    libgl1-mesa-dev \
    libxrandr-dev \
    libxxf86dga-dev \
    libxcursor-dev \
    bison \
    flex \
    libfreetype6-dev \
    libvorbis-dev \
    libeigen3-dev \
    libopenal-dev \
    libode-dev \
    libbullet-dev \
    nvidia-cg-toolkit \
    libgtk-3-dev \
    libassimp-dev \
    libopenexr-dev \
    git

WORKDIR /opt/toontown

# Copy files from the build context
COPY docker/libraries/panda3d1.11_1.11.0_amd64.deb ./
COPY docker/ai-server/entrypoint.sh ./
COPY src/requirements.txt ./
COPY config ./config

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

RUN dpkg -i panda3d1.11_1.11.0_amd64.deb
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]