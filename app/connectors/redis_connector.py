import redis.asyncio as redis

from app.logger import get_logger

logger = get_logger("redis")


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logger.info("Подключение к Redis: %s:%s", self.host, self.port)
        self.redis = await redis.Redis(host=self.host, port=self.port)
        try:
            await self.redis.ping()
        except redis.RedisError:
            logger.exception("Redis недоступен: %s:%s", self.host, self.port)
        else:
            logger.info("Redis подключён")

    async def set(self, key: str, value: str, expire: int | None = None):
        logger.debug("SET %s (expire=%s)", key, expire)
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        logger.debug("GET %s", key)
        return await self.redis.get(key)

    async def delete(self, key: str):
        logger.debug("DELETE %s", key)
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()
            logger.info("Соединение с Redis закрыто")


# Пример использования:
# redis_manager = RedisManager(redis_url="redis://localhost")
# await redis_manager.connect()
# await redis_manager.set("key", "value", expire=60)
# value = await redis_manager.get("key")
# await redis_manager.delete("key")
# await redis_manager.close()
