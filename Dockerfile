FROM armv7/armhf-ubuntu:xenial

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade --yes && \
    apt-get install --yes \
    owfs && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /mnt/1wire
