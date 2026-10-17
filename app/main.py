import logging
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from app.api.auth import router as router_auth
from app.api.bookings import router as router_bookings
from app.api.facilities import router as router_facilities
from app.api.hotels import router as router_hotels
from app.api.images import router as router_images
from app.api.rooms import router as router_rooms
from app.config import settings
from app.database import Base, engine
from app.exceptions import ApplicationExceptions
from app.init import redis_manager
from app.logger import get_logger, request_id_var, setup_logging

setup_logging()
logger = get_logger("app")
db_logger = get_logger("db")
http_logger = get_logger("http")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения (MODE=%s)", settings.MODE)
    db_logger.info("Подключение к PostgreSQL: %s", engine.url.render_as_string(hide_password=True))
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        db_logger.critical("Не удалось подключиться к PostgreSQL", exc_info=True)
        raise
    db_logger.info("PostgreSQL подключён, таблицы проверены")
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logger.info("Приложение запущено")
    yield
    logger.info("Остановка приложения")
    await engine.dispose()
    db_logger.info("Соединения с PostgreSQL закрыты")
    await redis_manager.close()
    logger.info("Приложение остановлено")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex[:8]
    token = request_id_var.set(request_id)
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        http_logger.exception("Необработанная ошибка: %s %s", request.method, request.url.path)
        raise
    else:
        duration_ms = (time.perf_counter() - start) * 1000
        if response.status_code >= 500:
            level = logging.ERROR
        elif response.status_code >= 400:
            level = logging.WARNING
        else:
            level = logging.INFO
        http_logger.log(
            level,
            "%s %s -> %s (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        request_id_var.reset(token)


@app.exception_handler(ApplicationExceptions)
async def application_exception_handler(request: Request, exc: ApplicationExceptions):
    http_logger.warning("%s: %s", type(exc).__name__, exc.detail)
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
