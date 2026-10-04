from app.models.bookings import BookingOrm
from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.models.rooms import RoomsOrm
from app.models.users import UsersOrm
from app.repositories.mappers.base import DataMapper
from app.models.hotels import HotelsOrm
from app.schemas.bookings import Booking
from app.schemas.facilities import Facilities, RoomsFacilities
from app.schemas.hotels import Hotel
from app.schemas.rooms import Room, RoomsWithRels
from app.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel

class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper):
    db_model = BookingOrm
    schema = Booking

class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities

class RoomFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomsFacilities

    
