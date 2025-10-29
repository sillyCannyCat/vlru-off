from ninja import Schema
from typing import List

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