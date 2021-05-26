#!/bin/sh

set -e

. /opt/pysetup/.venv/bin/activate

# выполняем необходимые таски перед запуском приложения
# python -m farfor_bot database upgrade


exec "$@"
