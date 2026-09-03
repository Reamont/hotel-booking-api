from app.repositories.base import BaseRepository
from app.models.facilities import FacilitiesOrm
from app.schemas.facilities import Facilities

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities