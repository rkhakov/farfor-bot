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
> farfor_bot database init --help

Usage: farfor_bot database init [OPTIONS]

  Инициализация базы
```


### default_records
Создает дефолтные записи в базе
```shell
> farfor_bot database default_records
> farfor_bot database default_records --help

Usage: farfor_bot database default_records [OPTIONS]

  Создает дефолтные записи в базе
```


### heads
Команда alembic heads, показывает заглавные ревизии
```shell
> farfor_bot database heads
> farfor_bot database heads --help

Usage: farfor_bot database heads [OPTIONS]

  Показать heads ревизий
```


### current
Команда alembic current, показывает последнюю применную ревизию в базе
```shell
> farfor_bot database current
> farfor_bot database current --help

Usage: farfor_bot database current [OPTIONS]

  Показать текущую версию ревизии в базе
```


### history
Команда alembic history, показывает историю ревизий
```shell
> farfor_bot database history 
> farfor_bot database history --help

Usage: farfor_bot database history [OPTIONS]

  Показать историю ревизий
```


### revision
Alimbic команда для создания ревизии. Название ревизии обязательно

```shell
> farfor_bot database revision -auto -m "message"
> farfor_bot database revision --help

Usage: farfor_bot database revision [OPTIONS]

  Создает ревизию

Options:
  -m, --message TEXT     Название ревизии  [required]
  -auto, --autogenerate  Автогенерация ревизии по последним изменениям в моделях
```


### upgrade
Alembic команда для применения ревизии.

```shell
> farfor_bot database upgrade
> farfor_bot database upgrade --help

Usage: farfor_bot database upgrade [OPTIONS]

  Обновить состояние базы до последней (или указанной) версии ревизии

Options:
  -r, --revision TEXT  Идентификатор ревизии
```


### downgrade
Alembic команда для отката ревизии

```shell
# Откат последней ревизии
> farfor_bot database downgrade -r -1
> farfor_bot database downgrade --help

Usage: farfor_bot database downgrade [OPTIONS]

  Откатить изменения

  Для того чтобы откатить последнюю ревизию, необходимо передать иденификатор ревизии -1

  Пример:     > farfof_bot database downgrade -r -1

Options:
  -r, --revision TEXT  Идентификатор ревизии
```

### drop
Удалить базу. Может пригодится на дев окружении

```shell
> farfor_bot database drop
> farfor_bot database drop --help
     
Usage: farfor_bot database drop [OPTIONS]

  Удалить базу

Options:
  --yes   Удалить базу без подтверждения
```


## telegram
Основные команды для управления телеграм ботом. Токен бота используется из кофигов проекта


### get_webhook
Получить URL вебхука установленного в телеграм боте

```shell
> farfor_bot telegram get_webhook
> farfor_bot telegram get_webhook --help

Usage: farfor_bot telegram get_webhook [OPTIONS]

  Получить установленный в боте URL вебхука
```


### set_webhook
Установить URL вебхука в телеграм боте. 
Будет установлен URL в том виде как он передан, без изменений

```shell
> farfor_bot telegram set_webhook --url "https://domain_name.com/webhook"
> farfor_bot telegram set_webhook --help

Usage: farfor_bot telegram set_webhook [OPTIONS]

  Установить URL вебхука для телеграм бота в том виде как он передан

  Протокол обязательно должен быть https

Options:
  --url TEXT  URL вебхука для телеграм бота  [required]
```

### delete_webhook
Удалить вебхук в телеграм боте. 

```shell
> farfor_bot telegram delete_webhook
> farfor_bot telegram delete_webhook --help

Usage: farfor_bot telegram delete_webhook [OPTIONS]

  Удалить установленный вебхук телеграм бота
```
