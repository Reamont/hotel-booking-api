from typing import Annotated

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.api.dependencies import DBdep
from app.schemas.facilities import FacilitiesAdd
from app.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=30)
async def get_all(db: DBdep):
    return await FacilityService(db).get_all()

@router.post("")
async def create_facility(db: DBdep, facility_data: Annotated[FacilitiesAdd, Body()]):
    facility = await FacilityService(db).create_facility(facility_data)

    return {"status": "OK", "data": facility}
