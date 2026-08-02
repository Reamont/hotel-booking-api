from fastapi import Query, APIRouter, Body
from app.api.dependencies import DBdep, UserIdDep
from app.schemas.bookings import BookingAddRequest, BookingAdd
from fastapi import HTTPException


router = APIRouter(prefix="/booking", tags=["Бронирования"])

@router.get("")
async def get_all(db: DBdep):
    return await db.bookings.get_all()

@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBdep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBdep,
    booking_data: BookingAddRequest = Body()
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price

    add_booking_data = BookingAdd(user_id=user_id,
                                  price=room_price,
                                  **booking_data.model_dump())

    booking = await db.bookings.add(add_booking_data)
    await db.commit()
    return {"status": "OK"}

#ffff


