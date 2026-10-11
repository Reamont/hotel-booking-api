from pydantic import BaseModel


class FacilitiesAdd(BaseModel):
    title: str

class Facilities(FacilitiesAdd):
    id: int

class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomsFacilities(RoomsFacilitiesAdd):
    id: int

