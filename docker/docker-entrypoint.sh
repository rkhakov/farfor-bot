#!/bin/sh

set -e

# тут запускаем скрипты необходимые перед запуском проекта

# накатываем миграции
farfor_bot database upgrade

exec "$@"
