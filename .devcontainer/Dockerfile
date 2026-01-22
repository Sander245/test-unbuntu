FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    sudo curl wget git \
    xfce4 xfce4-goodies tightvncserver dbus-x11 novnc websockify chromium \
    locales \
    && locale-gen en_US.UTF-8 \
    && apt-get clean
