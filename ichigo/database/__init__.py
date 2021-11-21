import functools
import logging
import typing
import asyncio
import asyncpg
import hikari


from ichigo.config.models import PostgresConfig
from ichigo.resources import get_resource
from ichigo.app import Ichigo

__all__ = ["Database"]

_LOGGER = logging.getLogger(__name__)

_any_callable = typing.Callable[..., typing.Any]


class Database:
    def __init__(self, bot: Ichigo, config: PostgresConfig) -> None:
        self.bot = bot
        self.config = config
        self._connected = asyncio.Event()
        self._pool: typing.Optional[asyncpg.Pool] = None

    @property
    def is_connected(self) -> bool:
        return self._connected.is_set()

    @property
    def pool(self) -> typing.Optional[asyncpg.Pool]:
        return self._pool

    async def initialise(self):
        assert not self.is_connected, "Already connected to database."

        _LOGGER.info("Creating connection pool")
        self._pool = await asyncpg.create_pool(**self.config.to_dict())

        _LOGGER.info("Syncing")
        self._connected.set()
        _LOGGER.info("executing schema")
        con: asyncpg.Connection
        async with self.pool.acquire() as con:
            async with con.transaction():
                schema: str
                with get_resource("schema.sql") as fp:
                    schema = fp.read()
                await con.execute(schema)

    async def close(self):
        assert self.is_connected, "Database is not connected."
        await self.pool.close()
        self._pool = None
        self._connected.clear()
        _LOGGER.info("Closed the database.")

    def in_transaction(c: _any_callable) -> _any_callable:
        @functools.wraps(c)
        async def wrap(self, *args, **kwargs):
            assert self.is_connected, "Database is not connected."
            con: asyncpg.Connection
            async with self._pool.acquire() as con:
                async with con.transaction():
                    await c(self, *args, con=con, **kwargs)

        return wrap

    # ! Example
    @in_transaction
    async def get_guild(self, guild_id: hikari.Snowflakeish, con: asyncpg.Connection):
        _LOGGER.info("works ig")
        _LOGGER.info(str(guild_id))
        _LOGGER.info(str(con))
        # return con.fetchrow(r"SELECT * FROM guilds WHERE guild_id = $1", int(guild_id))
