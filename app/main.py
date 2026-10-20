import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.DEBUG)

from app.api.auth import router as router_auth
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities
from app.api.hotels import router as router_hotels
from app.api.images import router as router_images
from app.api.rooms import router as router_rooms
from app.database import Base, engine
from app.exceptions import ApplicationExceptions
from app.init import redis_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logger.info("FastAPI cache initialized")
    logger.info("Приложение запущено")
    yield
    await engine.dispose()
    await redis_manager.close()
    logger.info("Приложение остановлено")


app = FastAPI(lifespan=lifespan)


@app.exception_handler(ApplicationExceptions)
async def application_exception_handler(request: Request, exc: ApplicationExceptions):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
