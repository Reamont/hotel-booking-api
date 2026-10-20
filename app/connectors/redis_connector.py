import logging

import redis.asyncio as redis

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logger.info(f"Начинаю подключение к Redis host={self.host}, port={self.port}")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logger.info(f"Успешное подключение к Redis host={self.host}, port={self.port}")

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()


# Пример использования:
# redis_manager = RedisManager(redis_url="redis://localhost")
# await redis_manager.connect()
# await redis_manager.set("key", "value", expire=60)
# value = await redis_manager.get("key")
# await redis_manager.delete("key")
# await redis_manager.close()
