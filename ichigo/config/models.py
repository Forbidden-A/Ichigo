# This is heavely inspired by Discord Coding Academy's Bracky Discord bot (https://gitlab.com/dcacademy/bracky).
import os
from typing import Type, TypeVar
import attr
import cattr

__all__ = ["BotConfig", "LoggingConfig", "PostgresConfig", "Config"]

ThisImplT = TypeVar("ThisImplT")


class BaseConfig:
    @classmethod
    def from_dict(
        cls: Type[ThisImplT],
        obj: dict[str, any],
        converter: cattr.Converter = cattr.global_converter,
    ) -> ThisImplT:
        return converter.structure(obj, cls)

    def to_dict(self) -> dict:
        assert attr.has(self.__class__)
        return attr.asdict(self)


@attr.s(frozen=True, auto_attribs=True)
class BotConfig(BaseConfig):
    """Some values related to the bot."""

    testing_guilds: list[str] = attr.ib(repr=False)
    token: str = attr.ib(repr=False, factory=lambda: os.environ["ICHIGO_TOKEN"])


@attr.s(frozen=True, auto_attribs=True)
class LoggingConfig(BaseConfig):
    """Configuration values for the root logger (set via the basicConfig function)."""

    level: str = "INFO"
    log_format: str = "{asctime} | {levelname:^8} | {name} :: {message}"
    date_format: str = "%a, %d, %b %Y (%H:%M:%S)"


@attr.s(frozen=True, auto_attribs=True)
class PostgresConfig(BaseConfig):
    """
    All values needed to connect to a PostgreSQL.
    The defaults will assume the bot is running on Docker.
    """

    password: str = attr.ib(repr=False, factory=lambda: os.environ["POSTGRES_PASSWORD"])
    host: str = "ichigo-db"
    port: int = 5432
    user: str = "postgres"
    database: str = "postgres"


@attr.s(frozen=True, auto_attribs=True)
class Config(BaseConfig):
    """Root configuration model."""

    bot: BotConfig = attr.ib(factory=BotConfig)
    logging: LoggingConfig = attr.ib(factory=LoggingConfig)
    database: PostgresConfig = attr.ib(factory=PostgresConfig)
