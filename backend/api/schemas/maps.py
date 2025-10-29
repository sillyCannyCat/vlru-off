from ninja import Schema
from typing import List, Optional
from datetime import datetime

class AddressSuggestion(Schema):
    type: str
    name: Optional[str] = None
    street: Optional[str] = None
    full_address: Optional[str] = None

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
    end_date: Optional[datetime] = None
    description: Optional[str]
    type: str
    initiator_name: Optional[str]
    source_name: Optional[str]
    buildings: List[BuildingOut]

class ComplaintSummaryOut(Schema):
    report_date: str
    summary: str
    complaint_count: int
    created_at: str

class ComplaintGraphItem(Schema):
    time: str
    cold_water: int
    hot_water: int
    electricity: int

class ComplaintGraphOut(Schema):
    data: List[ComplaintGraphItem]