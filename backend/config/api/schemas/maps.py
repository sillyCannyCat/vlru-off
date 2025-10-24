from ninja import Schema
from typing import List

class MapPoint(Schema):
    id: int
    name: str
    lat: float
    lon: float

class MapResponse(Schema):
    points: List[MapPoint]