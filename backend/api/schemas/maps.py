from ninja import Schema
from typing import List

class MapAddressOutItem(Schema):
    type: str
    coordinates: List[float]
    address: str
    description: str

class MapAddressOut(Schema):
    data: List[MapAddressOutItem]