from fastapi import APIRouter

from app.api.dependencies import DBdep, UserIdDep
from app.exceptions import check_dates
from app.schemas.bookings import BookingAdd, BookingAddRequest
from app.services.bookings import BookingService

router = APIRouter(prefix="/booking", tags=["Бронирования"])


@router.get("")
async def get_all(db: DBdep):
    return await BookingService(db).get_all()


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBdep):
    return await BookingService(db).get_me(user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBdep,
    booking_data: BookingAddRequest,
):
    booking = await BookingService(db).add_booking(user_id=user_id, booking_data=booking_data)
    
    return {"status": "OK", "data": booking}
