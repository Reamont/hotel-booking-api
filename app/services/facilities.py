from app.services.base import BaseService
from app.schemas.facilities import FacilitiesAdd
class FacilityService(BaseService):
    async def get_all(self):
        return await self.db.facilities.get_all()


    async def create_facility(self, facility_data: FacilitiesAdd):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        return facility