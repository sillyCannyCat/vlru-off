from ninja import Schema, Field
from typing import List, Optional
from datetime import datetime

class BuildingOut(Schema):
    building_id: str
    street_name: Optional[str]
    number: int
    district_name: Optional[str]
    folk_district_name: Optional[str]
    latitude: float
    longitude: float

class BlackoutOut(Schema):
    blackout_id: str
    start_date: datetime
    end_date: Optional[datetime] = Field(None, alias='end_data')
    description: Optional[str]
    type: str
    initiator_name: Optional[str]
    source_name: Optional[str]
    buildings: List[BuildingOut]

class AddressIn(Schema):
    address: str