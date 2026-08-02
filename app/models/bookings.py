from datetime import date

from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Base

class BookingOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self):
        return self.price * (self.date_to - self.date_from).days