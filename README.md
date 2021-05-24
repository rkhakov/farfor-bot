# Телеграм бот
Микросервис отправляющий сообщения сотрудникам Фарфор в телеграм бот
На данный момент используется только для отправки событий с камер контроля качества из проекта smenateam/farfor


## Документация
* [Начало работы](/docs/getting_started.md)
* [Утилиты командной строки (CLI)](/docs/cli.md)


## TODO
* [x] FastAPI
* [x] Конфиги vscode для запуска проекта
* [ ] Конфиг логгера
* [ ] Sentry
* [ ] Прекоммит хуки
* [ ] OAuth
    * [x] Получение токена
    * [ ] Проверка токена
    * [ ] Сброс пароля
* [ ] API Управления пользователями (superuser)
    * [ ] Список
    * [ ] Создание
    * [ ] Получение
    * [ ] Обновление
    * [ ] Удаление
    * [ ] Регистрация
* [ ] API Управления телеграм пользователями (superuser)
    * [ ] Список
    * [ ] Создание
    * [ ] Получение
    * [ ] Обновление
    * [ ] Удаление
* [ ] API Управления вебхуком телеграм
    * [ ] Вебхук
    * [ ] Установка вебхука
    * [ ] Удаление вебхука
    * [ ] Получение информации о вебхуке
* [ ] Broadcast
    * [ ] Получение актиных пользователей телеграм по точке (менеджеров)
    * [ ] Получение активных пользователей телеграм по городу (супервизоров) ? Если нужно будет
    * [ ] Получение активных пользователей администраторов ? Если нужно будет
    * [ ] Отправка события камеры в телеграм полученным пользователям
* [x] Конфиги проекта
* [x] SQLAlchemy
* [x] Alembic
* [ ] CLI
    * [ ] Управление сервером
        * [x] Запуск develop окружения
        * [ ] Запуск продового окружения
        * [x] Запуск shell
        * [x] Отображение конфига
    * [x] База
        * [x] Инициализация базы
        * [x] Применение миграций
        * [x] Создание миграции
        * [x] Откат изменений
        * [x] Удаление базы
        * [x] Дамп
        * [x] Восстановление из дампа
