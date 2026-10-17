from typing import Annotated

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.api.dependencies import DBdep
from app.logger import get_logger
from app.schemas.facilities import FacilitiesAdd
from app.tasks.tasks import test_task

logger = get_logger("facilities")

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=30)
async def get_all(db: DBdep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBdep, facility_data: Annotated[FacilitiesAdd, Body()]):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    logger.info("Создано удобство id=%s: %s", facility.id, facility.title)

    test_task.delay()
    logger.debug("Задача test_task поставлена в очередь")

    return {"status": "OK", "data": facility}
