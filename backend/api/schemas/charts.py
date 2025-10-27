from ninja import Schema
from typing import List, Dict, Optional
from datetime import date

class StatsByType(Schema):
    type: str
    count: int

class StatsByDistrict(Schema):
    district_name: str
    count: int

class TimelineStats(Schema):
    date: date
    count: int

class ChartFilterIn(Schema):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    type: Optional[str] = None