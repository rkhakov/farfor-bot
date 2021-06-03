# CLI
Интерфейс командной строки для управления проектом

> Вся работа с проектом должна происходить с использованием CLI. 
> Если чего то не хватает, то лучше добавить это и задокументировать

Все утилиты собраны в файле `farfor_bot/__main__.py`. 
Поэтому их можно запускать как python модуль из под виртуального окружения

```shell
> python -m farfor_bot --help
```

или через poetry
```shell
> poetry run farfor_bot --help
```

Данная команда добавлена в `pyproject.toml`,
поэтому она также будет доступна после сборки и установки приложения
как зависимость в `bin` виртуального окружения.

В последующих примерах `poetry run` будет опущен

## Документация по командам
Передав опцию `--help` для группы или команды, будет выведена вспомогательная информация 
```shell
> farfor_bot --help
> farfor_bot database --help
> farfor_bot database revision --help
```

## server
Содержит основные команды для работы с сервером


### config
Отображает таблицу с конфигами проекта. Помогает для дебага

```shell
> farfor_bot server config

Key                          Value
---------------------------  ------------------------------------------------------------
PROJECT_NAME                 Farfor Bot
ACCESS_TOKEN_EXPIRE_MINUTES  11520
SECRET_KEY                   HACKME
DEFAULT_USER_LOGIN           admin
DEFAULT_USER_PASSWORD        admin
TELEGRAM_TOKEN               TOKEN
DATABASE_HOST                127.0.0.1
DATABASE_PORT                44444
DATABASE_USER                postgres
DATABASE_PASSWORD            postgres
DATABASE_NAME                farforbot
SQLALCHEMY_DATABASE_URI      postgresql://postgres:postgres@192.168.0.105:44444/farforbot
```


### develop
Стартует дев сервер с hot reload при изменениях в файлах проекта

```shell
> farfor_bot server develop
```

По дефолту запускается на порту `8900`. Порт можно указать опцией `--port`
```shell
> farfor_bot server develop --port 8000
```


### shell
Запускает IPython shell. Работает только на dev окружении.

```shell
> farfor_bot server shell
```


## database
Команды для управления состоянием базы

```shell
> farfor_bot database --help

Usage: farfor_bot database [OPTIONS] COMMAND [ARGS]...

  Команды для управления состоянием базы данных

Options:
  --help  Show this message and exit.

Commands:
  current          Показать текущую версию ревизии в базе
  default_records  Создать дефолтные записи в базе
  downgrade        Откатить изменения Для того чтобы откатить последнюю...
  drop             Удалить базу
  heads            Показать heads ревизий
  history          Показать историю ревизий
  init             Инициализировать базу
  revision         Создать ревизию
  upgrade          Обновить состояние базы до последней (или указанной)...

```

### init
Инициализирует базу и запускает ревизии
```shell
> farfor_bot database init
```


### create_superuser
Создать супер пользователя
```shell
> farfor_bot database create_superuser --login admin --password admin
```


### heads
Команда alembic heads, показывает заглавные ревизии
```shell
> farfor_bot database heads
```


### current
Команда alembic current, показывает последнюю применную ревизию в базе
```shell
> farfor_bot database current
```


### history
Команда alembic history, показывает историю ревизий
```shell
> farfor_bot database history
```


### revision
Alimbic команда для создания ревизии. Название ревизии обязательно

```shell
> farfor_bot database revision -auto -m "message"
```


### upgrade
Alembic команда для применения ревизии.

```shell
> farfor_bot database upgrade
```


### downgrade
Alembic команда для отката ревизии

```shell
# Откат последней ревизии
> farfor_bot database downgrade -r -1
```

### drop
Удалить базу. Может пригодится на дев окружении

```shell
> farfor_bot database drop
```


## telegram
Основные команды для управления телеграм ботом. Токен бота используется из кофигов проекта


### get_webhook
Получить URL вебхука установленного в телеграм боте

```shell
> farfor_bot telegram get_webhook
```


### set_webhook
Установить URL вебхука в телеграм боте. 
Будет установлен URL в том виде как он передан, без изменений

```shell
> farfor_bot telegram set_webhook --url "https://domain_name.com/webhook"
```

### delete_webhook
Удалить вебхук в телеграм боте. 

```shell
> farfor_bot telegram delete_webhook
```
