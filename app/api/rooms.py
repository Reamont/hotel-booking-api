from datetime import date

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBdep
from app.schemas.facilities import RoomsFacilitiesAdd
from app.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotel", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int, 
    db: DBdep,
    date_from: date = Query(examples=["2026-09-03"]),
    date_to: date = Query(examples=["2026-09-03"])
    ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,date_from=date_from, date_to=date_to)



@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBdep):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)



@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBdep, room_data: RoomAddRequest = Body()):
    add_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(add_room_data)

    room_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=facility_id) for facility_id in room_data.facilities_ids or []]
    if room_facilities_data:
        await db.rooms_facilities.add_many(room_facilities_data)
    await db.commit()
    return {"status": "OK", "data": add_room_data}



@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBdep,
):
    edit_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update(edit_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids or [])
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBdep,
):
    room_data_dict = room_data.model_dump(exclude_unset=True)
    patch_room_data = RoomPatch(hotel_id=hotel_id, **room_data_dict)
    await db.rooms.update(patch_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data_dict["facilities_ids"] or [])
    await db.commit()
    return {"status": "OK"}



@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBdep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

    



