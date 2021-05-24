# CLI
Утилиты командной строки для управления проектом

> Вся работа с проектом должна происходить с использованием CLI. Если чего то не хватает, то лучше добавить это и задокументировать

Все утилиты собраны в файле `farfor_bot/__main__.py`. Поэтому их можно запускать как python модуль

```shell
> python -m farfor_bot --help
```

или через poetry
```shell
> poetry run farfor_bot --help
```

Данная команда добавлена в `pyproject.toml` поэтому она также будет доступна после сборки и установки приложения как зависимость в `bin` виртуального окружения.

В последующих примерах будет использоваться только команда `farfor_bot`


## Документация по командам
Как было показано выше в примерах, для получения списка доступных групп или команд необходимо передать флаг `--help `
```shell
> farfor_bot --help
> farfor_bot database --help
> farfor_bot database revision --help
```

## Server
Содержит все команды для работы с сервером


### Config
Отображает таблицу с конфигами проекта. Помогает для дебага

```shell
> farfor_bot server config

Key                          Value
---------------------------  ----------------
PROJECT_NAME                 Farfor Bot
DEV_SERVER_PORT              8900
ACCESS_TOKEN_EXPIRE_MINUTES  11520
SECRET_KEY                   SECRET
DATABASE_HOST                127.0.0.1
DATABASE_PORT                44444
DATABASE_USER                postgres
DATABASE_PASSWORD            postgres
DATABASE_NAME                farforbot
```

### Develop
Стартует дев сервер с авторестартом при изменениях в файлах проекта

```shell
> farfor_bot server develop
```


### Shell
Запускает IPython shell. Работает только на dev окружении.

```shell
> farfor_bot server shell
```


## Database
Команды для управления базой

```shell
> farfor_bot database --help

Usage: farfor_bot database [OPTIONS] COMMAND [ARGS]...

  Команды для управления состоянием базы данных

Options:
  --help  Show this message and exit.

Commands:
  downgrade  Откатить изменения Для того чтобы откатится на предыдущую...
  drop       Удалить базу
  dump       Дамп базы
  init       Инициализация базы
  revision   Создает ревизию
  upgrade    Обновить состояние базы до последней (или указанной) версии...
```

### Init
Инициализирует базу и создает необходимые таблицы
```shell
> farfor_bot database init
```

### Revision
Alimbic команда для создания ревизии. Название ревизии (-m -message) обязательно

```shell
> farfor_bot database revision -auto -m "message"
> farfor_bot database revision --help

Создает ревизию

Options:
  -m, --message TEXT     Название ревизии  [required]
  -auto, --autogenerate  Автогенерация ревизии по последним изменениям в моделях
```