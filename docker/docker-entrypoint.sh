#!/bin/sh

set -e

# тут запускаем скрипты необходимые перед запуском проекта

# накатываем миграции
farfor_bot database upgrade

# создаем дефолтные записи в базе, если не созданы
farfor_bot database default_records

exec "$@"
