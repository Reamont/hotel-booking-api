from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
from contextlib import asynccontextmanager

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.api.auth import router as router_auth
from app.api.rooms import router as router_rooms
from app.api.bookings import router as router_bookings

from app.database import Base, engine
from app.config import settings

from app.models.hotels import HotelsOrm
from app.models.rooms import RoomsOrm

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(settings.DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Приложение запущено")
    yield
    await engine.dispose()
    print("Приложение остановлено")

app = FastAPI(lifespan=lifespan)


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)


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