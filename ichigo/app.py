import logging
import os
import pathlib
import hikari

import lightbulb
from ichigo import extensions

from ichigo.config.load import deserialise_raw_config, load_config_file
from ichigo.config.models import Config
from ichigo.database import Database

__all__ = ["Ichigo"]

_LOGGER = logging.getLogger(__name__)


class Ichigo(lightbulb.BotApp):

    CONFIG_PATH = os.environ.get("ICHIGO_CONFIG_PATH") or "./config.yml"
    CONFIG_CACHE = deserialise_raw_config(load_config_file(CONFIG_PATH), True)

    def __init__(self) -> None:
        super().__init__(
            intents=hikari.Intents.ALL_GUILDS_UNPRIVILEGED
            | hikari.Intents.GUILD_MEMBERS,
            token=self.config.bot.token,
        )

        subscriptions = {
            hikari.events.StartingEvent: self.on_starting,
            hikari.events.StartedEvent: self.on_started,
            hikari.events.ShardReadyEvent: self.on_shard_ready,
        }

        for event, callback in subscriptions.items():
            self.subscribe(event, callback)

    @property
    def config(self) -> Config:
        if Ichigo.CONFIG_CACHE is None:
            Ichigo.CONFIG_CACHE = deserialise_raw_config(
                load_config_file(Ichigo.CONFIG_PATH)
            )
        return Ichigo.CONFIG_CACHE

    async def on_starting(self, _: hikari.StartingEvent):
        _LOGGER.info("Bot is Starting..")
        _LOGGER.info("Connecting to database..")
        self._database = Database(self, Ichigo.CONFIG_CACHE.database)
        await self.database.initialise()
        _LOGGER.info("Loading extensions")
        self.load_extensions_from(pathlib.Path(os.path.realpath(extensions.__file__)))

    async def on_started(self, _: hikari.StartedEvent):
        pass

    async def on_shard_ready(self, _: hikari.ShardReadyEvent):
        pass
