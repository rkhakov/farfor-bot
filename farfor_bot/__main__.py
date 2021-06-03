"""CLI проекта"""
import os

import click
import uvicorn
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from tabulate import tabulate

from farfor_bot import __version__
from farfor_bot.config import settings
from farfor_bot.database.core import Base, engine


ALEMBIC_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "database/alembic.ini"
)


@click.group()
@click.version_option(version=__version__)
def farfor_bot():
    pass


@farfor_bot.group("server")
def server():
    """Команды для управления сервером"""
    pass


@server.command("develop")
@click.option(
    "--port",
    default=8900,
    help="Порт запускаемого uvicorn приложения. По умолчанию 8900",
)
@click.option("--log-level", default="debug", help="Уровень логов")
def run_server(log_level: str, port: int):
    """Запустить дев сервер"""
    uvicorn.run(
        "farfor_bot.main:app",
        debug=True,
        log_level=log_level,
        port=port,
    )


@server.command("shell")
@click.argument("ipython_args", nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    """Запусть Shell IPython"""
    import sys

    import IPython
    from IPython.terminal.ipapp import load_default_config

    config = load_default_config()

    banner = f"Python {sys.version} on {sys.platform} IPython: {IPython.__version__}"
    config.TerminalInteractiveShell.banner1 = banner

    IPython.start_ipython(argv=ipython_args, user_ns={}, config=config)


@server.command("config")
def show_config():
    """Показать конфиги"""
    table = []
    for key, value in settings:
        if key.isupper():
            table.append([key, value])

    click.secho(tabulate(table, headers=["Key", "Value"]), fg="blue")


@farfor_bot.group("database")
def database():
    """Команды для управления состоянием базы данных"""
    pass


@database.command("init")
def init_database():
    """Инициализировать базу"""
    from sqlalchemy_utils import create_database, database_exists

    if not database_exists(settings.SQLALCHEMY_DATABASE_URI):
        create_database(settings.SQLALCHEMY_DATABASE_URI)

    Base.metadata.create_all(engine)
    alimbic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.stamp(alimbic_cfg, "head")

    click.secho("База создана", fg="green")


@database.command("create_superuser")
@click.option("--login", required=True, help="Логин")
@click.option("--password", required=True, help="Пароль")
def create_superuser(login, password):
    """Создать супер пользователя"""

    from farfor_bot.database.core import SessionLocal
    from farfor_bot.repositories import user_repository
    from farfor_bot.schemas import UserCreateSchema

    db_session = SessionLocal()

    user_schema = UserCreateSchema(
        login=login,
        password=password,
        is_active=True,
        is_admin=True,
        is_superuser=True,
    )
    if not user_repository.get_by_login(db_session, login=user_schema.login):
        user_repository.create(db_session, obj_schema=user_schema)
        click.secho(f"Пользователь {login} создан", fg="green")
    else:
        click.secho(f"Пользователь {login} уже существует", fg="red")


@database.command("heads")
def heads():
    """Показать heads ревизий"""
    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.heads(alembic_cfg)


@database.command("current")
def current_database():
    """Показать текущую версию ревизии в базе"""
    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.current(alembic_cfg)


@database.command("history")
def history_database():
    """Показать историю ревизий"""
    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.history(alembic_cfg)


@database.command("revision")
@click.option("-m", "--message", required=True, help="Название ревизии")
@click.option(
    "-auto",
    "--autogenerate",
    is_flag=True,
    help=("Автогенерация ревизии по последним изменениям в моделях"),
)
def revision_database(message, autogenerate):
    """Создать ревизию"""
    import time

    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.revision(
        alembic_cfg,
        message,
        autogenerate=autogenerate,
        sql=False,
        head="head",
        splice=False,
        branch_label=None,
        version_path=None,
        rev_id=str(int(time.time())),
    )


@database.command("upgrade")
@click.option("-r", "--revision", nargs=1, default="head", help="Идентификатор ревизии")
def upgrade_database(revision):
    """Обновить состояние базы до последней (или указанной) версии ревизии"""
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy_utils import create_database, database_exists

    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    if not database_exists(settings.SQLALCHEMY_DATABASE_URI):
        create_database(settings.SQLALCHEMY_DATABASE_URI)
        Base.metadata.create_all(engine)
        alembic_command.stamp(alembic_cfg, "head")
    else:
        conn = engine.connect()
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        if not current_rev:
            Base.metadata.create_all(engine)
            alembic_command.stamp(alembic_cfg, "head")
        else:
            alembic_command.upgrade(alembic_cfg, revision, sql=False, tag=None)

    click.secho("Успешно", fg="green")


@database.command("downgrade")
@click.option("-r", "--revision", nargs=1, default="head", help="Идентификатор ревизии")
def downgrade_database(revision):
    """
    Откатить изменения

    Для того чтобы откатить последнюю ревизию,
     необходимо передать иденификатор ревизии -1

    Пример:
        > farfof_bot database downgrade -r -1
    """
    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.downgrade(alembic_cfg, revision, sql=False, tag=None)
    click.secho("Успешно", fg="green")


@database.command("drop")
@click.option("--yes", is_flag=True, help="Удалить базу без подтверждения")
def drop_database(yes):
    """Удалить базу"""
    from sqlalchemy_utils import drop_database

    if yes:
        drop_database(settings.SQLALCHEMY_DATABASE_URI)
        click.secho("Success.", fg="green")

    if click.confirm(
        f"Вы уверены что хотите удалить базу: "
        f"'{settings.DATABASE_HOST}:{settings.DATABASE_NAME}'?"
    ):
        drop_database(settings.SQLALCHEMY_DATABASE_URI)
        click.secho("База удалена", fg="green")


@farfor_bot.group("telegram")
def telegram():
    """Команды для управления телеграм ботом"""
    pass


@telegram.command("get_webhook")
def get_webhook():
    """Получить установленный в боте URL вебхука"""
    from farfor_bot.services import telegram_service

    webhook_info = telegram_service.get_webhook_info()
    if webhook_info.url:
        table = []
        for key, value in webhook_info:
            table.append([key, value])
        click.secho(tabulate(table, headers=["Key", "Value"]), fg="blue")
    else:
        click.secho("Вебхук не установлен", fg="yellow")


@telegram.command("set_webhook")
@click.option("--url", required=True, help="URL вебхука для телеграм бота")
def set_webhook(url):
    """
    Установить URL вебхука для телеграм бота в том виде как он передан

    Протокол обязательно должен быть https
    """
    from farfor_bot.services import telegram_service

    if telegram_service.set_webhook(url):
        click.secho("Вебхук установлен", fg="green")
    else:
        click.secho("Ошибка: Вебхук не установлен", fg="red")


@telegram.command("delete_webhook")
def delete_webhook():
    """Удалить установленный вебхук телеграм бота"""
    from farfor_bot.services import telegram_service

    telegram_service.delete_webhook()
    click.secho("Вебхук удален", fg="green")


def entrypoint():
    farfor_bot()


if __name__ == "__main__":
    entrypoint()
