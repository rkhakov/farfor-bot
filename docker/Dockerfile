# Создаем базовый образ и устанавливаем переменные окружения
FROM python:3.9-slim as python-base

ENV PYTHONBUFFERED=1 \
    # Отключаем .pyc
    PYTHONDONTWRITEBYTECODE=1 \
    # Отключаем warnings
    PYTHONWARNINGS="ignore" \
    \
    # PIP
    # Отключаем кеширование
    PIP_NO_CACHE_DIR=off \
    # Отключаем проверку версии
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # Меняем дефолтный таймаут сокета
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # POETRY
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.6 \
    # Задаем директорию для poetry
    POETRY_HOME="/opt/poetry" \
    # включаем создание .venv внутри проекта
    # .venv будет создан там где запускается poetry install
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # отключаем интерактивные вопросы poetry
    POETRY_NO_INTERACTION=1 \
    \
    # Пути
    # директория в которую будет скопирован проект для сборки
    PROJECT_SETUP_PATH="/opt/project_setup" \
    # Директория виртуального окружения
    VENV_PATH="/opt/project_setup/.venv"

# Добавляем в PATH бинари poetry и .venv
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# Образ для сборки
FROM python-base as builder

# curl - для установки poetry
# build-essential - для сборки python зависимостей
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential

# Устанавливаем poetry. Версия и путь для установки заданы в env
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Меняем рабочую директорию
WORKDIR $PROJECT_SETUP_PATH

# Копируем, билдим и устанавливаем
COPY ./poetry.lock ./pyproject.toml ./
COPY ./farfor_bot ./farfor_bot

RUN poetry build

RUN pip install -U ./dist/*.whl

# Образ для прода
FROM python-base as production
ENV PROJECT_ENV=production

COPY --from=builder $VENV_PATH $VENV_PATH
COPY ./docker/gunicorn_conf.py /gunicorn_conf.py
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--config", "/gunicorn_conf.py", "farfor_bot.main:app"]
