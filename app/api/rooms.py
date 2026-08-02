from fastapi import Query, APIRouter, Body

from app.api.dependencies import DBdep
from app.schemas.rooms import RoomAddRequest, RoomAdd, Room, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotel", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBdep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBdep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBdep, room_data: RoomAddRequest = Body()):
    add_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.add(add_room_data)
    await db.commit()
    return {"status": "OK", "data": add_room_data}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, db: DBdep, room_data: RoomPatchRequest = Body()):
    edit_room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(edit_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_edit_hotel(hotel_id: int, db: DBdep, room_id: int, room_data: RoomPatchRequest):
    patch_room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(patch_room_data, id=room_id, hotel_id=hotel_id, exclude_unset = True)
    await db.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBdep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

    



