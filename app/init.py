from app.config import settings
from app.connectors.redis_connector import RedisManager

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
