from ichigo.app import *  # noqa
from ichigo.config import *  # noqa
from ichigo.database import *  # noqa
from ichigo.resources import *  # noqa


__version__ = "0.1.0"
__authors__ = ["Forbidden-A", "randomcmd"]


def main() -> None:
    import logging

    logging.basicConfig(
        level=Ichigo.CONFIG_CACHE.logging.level,
        style="{",
        format=Ichigo.CONFIG_CACHE.logging.log_format,
        datefmt=Ichigo.CONFIG_CACHE.logging.date_format,
    )

    bot = Ichigo()
    bot.run()
