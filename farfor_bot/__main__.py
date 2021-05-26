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
def run_server(log_level: str = "debug"):
    # TODO Добавить выбор уровня логов
    uvicorn.run(
        "farfor_bot.main:app",
        debug=True,
        log_level=log_level,
        port=settings.DEV_SERVER_PORT,
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
    """Инициализация базы"""
    from sqlalchemy_utils import create_database, database_exists

    if not database_exists(settings.SQLALCHEMY_DATABASE_URI):
        create_database(settings.SQLALCHEMY_DATABASE_URI)

    Base.metadata.create_all(engine)
    alimbic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.stamp(alimbic_cfg, "head")

    # Создаем дефолтные записи в БД

    click.secho("Success.", fg="green")


@database.command("revision")
@click.option("-m", "--message", required=True, help="Название ревизии")
@click.option(
    "-auto",
    "--autogenerate",
    is_flag=True,
    help=("Автогенерация ревизии по последним изменениям в моделях"),
)
def revision_database(message, autogenerate):
    """Создает ревизию"""
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

    click.secho("Success.", fg="green")


@database.command("downgrade")
@click.option("-r", "--revision", nargs=1, default="head", help="Идентификатор ревизии")
def downgrade_database(revision):
    """
    Откатить изменения

    Для того чтобы откатится на предыдущую ревизию, необходимо передать -1

    Пример:
        > farfof_bot database downgrade -r -1
    """
    alembic_cfg = AlembicConfig(ALEMBIC_PATH)
    alembic_command.downgrade(alembic_cfg, revision, sql=False, tag=None)
    click.secho("Success.", fg="green")


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
        click.secho("Success.", fg="green")


@database.command("dump")
@click.option(
    "--dump-file",
    default="farfor-bot-backup.dump",
    help="Файл куда будет сохранен дамп",
)
def dump_database(dump_file):
    """Дамп базы"""
    try:
        from sh import pg_dump
    except ImportError:
        click.secho("Утилита pg_dump не найдена", fg="red")
        return

    pg_dump(
        "-f",
        dump_file,
        "-h",
        settings.DATABASE_HOST,
        "-p",
        settings.DATABASE_PORT,
        "-U",
        settings.DATABASE_USER,
        settings.DATABASE_NAME,
        _env={"PGPASSWORD": settings.DATABASE_PASSWORD},
    )


def entrypoint():
    farfor_bot()


if __name__ == "__main__":
    entrypoint()
