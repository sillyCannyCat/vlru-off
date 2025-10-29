from ninja import Schema
from typing import List

class MapAddressOutItem(Schema):
    type: str
    coordinates: str
    address: str
    description: str
    coordinates: str

class MapAddressOut(Schema):
    data: List[MapAddressOutItem]