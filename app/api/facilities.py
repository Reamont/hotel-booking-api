import json

from fastapi import Query, APIRouter, Body
from app.api.dependencies import DBdep
from app.schemas.facilities import FacilitiesAdd
from app.init import redis_manager

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_all(db: DBdep):
    facilities_from_cache = redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts



@router.post("")
async def create_facility(db: DBdep, facility_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}


