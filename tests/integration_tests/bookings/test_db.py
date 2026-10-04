from datetime import date

from app.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.date_from == new_booking.date_from
    assert booking.date_to == new_booking.date_to
    assert booking.price == new_booking.price

    updated_date = date(year=2024, month=1, day=25)
    update_booking_data = booking_data.model_copy(update={"date_from": updated_date})
    await db.bookings.update(update_booking_data, id=new_booking.id)

    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.date_from == updated_date

    await db.bookings.delete(id = new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is None

    await db.commit()