from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Query

from app.api.dependencies import DBdep
from app.schemas.rooms import RoomAddRequest, RoomPatchRequest
from app.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBdep,
    date_from: Annotated[date, Query(examples=["2026-09-03"])],
    date_to: Annotated[date, Query(examples=["2026-09-04"])],
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBdep):
    return await RoomService(db).get_room(hotel_id, room_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBdep, room_data: Annotated[RoomAddRequest, Body()]):
    room = await RoomService(db).create_room(hotel_id, room_data)
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
    db: DBdep,
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBdep,
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBdep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}
