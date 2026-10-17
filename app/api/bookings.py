from fastapi import APIRouter

from app.api.dependencies import DBdep, UserIdDep
from app.exceptions import check_dates
from app.logger import get_logger
from app.schemas.bookings import BookingAdd, BookingAddRequest

logger = get_logger("bookings")

router = APIRouter(prefix="/booking", tags=["Бронирования"])


@router.get("")
async def get_all(db: DBdep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBdep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBdep,
    booking_data: BookingAddRequest,
):
    check_dates(booking_data.date_from, booking_data.date_to)
    room = await db.rooms.get_one(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room.price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    await db.commit()
    logger.info(
        "Создано бронирование id=%s: user_id=%s, room_id=%s, %s — %s",
        booking.id,
        user_id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    return {"status": "OK", "data": booking}
