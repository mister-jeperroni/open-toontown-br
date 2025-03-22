# Use uma imagem base com Ubuntu
FROM ubuntu:20.04

# Evita que a interação do terminal seja necessária durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualize o sistema e instale as dependências
RUN apt-get update && apt-get install -y \
    libboost-dev \
    wget \
    cmake \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    unzip \
    libyaml-cpp-dev \
    libuv1-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar o mongo-c-driver
RUN mkdir -p ~/build && cd ~/build && \
    wget https://github.com/mongodb/mongo-c-driver/releases/download/1.13.0/mongo-c-driver-1.13.0.tar.gz && \
    tar xzf mongo-c-driver-1.13.0.tar.gz && \
    cd mongo-c-driver-1.13.0 && \
    cmake -DENABLE_ZLIB=BUNDLED -DENABLE_SSL=OPENSSL . && \
    make && \
    make install

# Instalar o mongo-cxx-driver
RUN mkdir -p ~/build && cd ~/build && \
    wget https://github.com/mongodb/mongo-cxx-driver/archive/r3.4.0.tar.gz && \
    tar xzf r3.4.0.tar.gz && \
    cd mongo-cxx-driver-r3.4.0/build && \
    cmake .. && \
    make && \
    make install && \
    cp -r install/* /usr/local

# Criar diretórios necessários
RUN mkdir -p /opt/astron/config \
    && mkdir -p /opt/astron/etc

# Copiar arquivos de configuração
COPY docker/libraries/astrond_with_mongo /opt/astron/astrond

COPY config/astrond.yml /opt/astron/config/astrond.yml
COPY config/otp.dc /opt/astron/config/
COPY config/toon.dc /opt/astron/config/

# Defina o diretório de trabalho
WORKDIR /opt/astron

# Comando para rodar o contêiner (ajuste conforme necessário)
CMD ["./astrond", "--loglevel", "info", "/opt/astron/config/astrond.yml"]
