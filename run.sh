#!/bin/bash

# Сборка образа
docker build -t currency-rates /home/koshsky/tmp

# Предоставление доступа к X-серверу
xhost +local:docker

# Запуск контейнера с необходимыми параметрами для GUI
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network host \
    currency-rates
