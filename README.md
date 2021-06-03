# Телеграм бот
Микросервис отправляющий сообщения сотрудникам Фарфор в телеграм бот.

> На данный момент используется только для отправки событий с камер контроля качества из проекта smenateam/farfor


## Документация
* [Начало работы](/docs/getting_started.md)
* [Интерфейс командной строки (CLI)](/docs/cli.md)


## TODO
* [x] Конфиги vscode pycharm для запуска проекта
* [ ] Конфиг логгера
* [ ] Sentry
* [ ] Обработка ошибок orm
* [x] Прекоммит хуки
* [x] Docker
* [x] k8s
* [x] auto scale
* [ ] ssl
* [ ] CI/CD
* [ ] Frontend
* [ ] Health check
* [ ] locust
* [ ] Тесты
  * [ ] Stairway тест миграций
  * [ ] API
  * [ ] coverage
* [x] OAuth
    * [x] Аутентификация
    * [x] Проверка токена
* [x] API Управления пользователями (superuser)
    * [x] Список
    * [x] Создание
    * [x] Получение
    * [x] Обновление
    * [x] Удаление
* [x] API Управление сотрудниками (admin)
    * [x] Список
    * [x] Создание
    * [x] Получение
    * [x] Обновление
    * [x] Удаление
* [x] API Управления вебхуком телеграм
    * [x] Вебхук
    * [x] Установка вебхука
    * [x] Удаление вебхука
    * [x] Получение информации о вебхуке
* [x]  Отправка события с камеры сотрудникам в телеграм
* [x] Конфиги проекта
* [x] SQLAlchemy
* [x] Alembic
* [x] CLI
    * [x] Управление сервером
        * [x] Запуск develop окружения
        * [x] Запуск shell
        * [x] Отображение конфига
    * [x] База
        * [x] Инициализация базы
        * [x] Применение миграций
        * [x] Создание миграции
        * [x] Откат изменений
        * [x] Удаление базы
    * [x] Телеграм