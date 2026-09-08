from pydantic import BaseModel, Field, ConfigDict

from app.schemas.facilities import Facilities

class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = []

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

class RoomsWithRels(Room):
    facilities: list[Facilities]

class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = []

class RoomPatch(BaseModel):
    hotel_id: int
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None