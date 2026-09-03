from fastapi import Query, APIRouter, Body
from app.api.dependencies import DBdep
from app.schemas.facilities import FacilitiesAdd
from fastapi import HTTPException

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_all(db: DBdep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(id: int, db: DBdep, facility_data: FacilitiesAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}


