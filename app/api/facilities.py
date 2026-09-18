from fastapi_cache.decorator import cache

from fastapi import APIRouter, Body
from app.api.dependencies import DBdep
from app.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@cache(expire=30)
async def get_all(db: DBdep):
     return await db.facilities.get_all()





@router.post("")
async def create_facility(db: DBdep, facility_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}


