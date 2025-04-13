#!/bin/bash

# Перенаправляем вывод в лог-файл
exec 1> "${HOME}/.currency-rates.log" 2>&1

# Проверяем, существует ли образ
if ! docker image inspect currency-rates >/dev/null 2>&1; then
    # Если образ не существует, собираем его
    docker build -t currency-rates "$(dirname "$0")"
fi

# Предоставление доступа к X-серверу
xhost +local:docker >/dev/null 2>&1

# Запуск контейнера с необходимыми параметрами для GUI
docker run -d --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network host \
    currency-rates
