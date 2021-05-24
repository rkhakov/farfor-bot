"""CLI проекта"""
import click
import uvicorn

from farfor_bot import __version__
from farfor_bot.config import settings


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
    uvicorn.run("farfor_bot.main:app", debug=True, log_level=log_level, port=settings.DEV_SERVER_PORT)


def entrypoint():
    farfor_bot()


if __name__ == "__main__":
    entrypoint()
