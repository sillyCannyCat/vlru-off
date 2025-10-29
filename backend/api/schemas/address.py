from ninja import Schema
from typing import List

class AddressAutocompleteItem(Schema):
    type:str
    address: str

class AddressAutocompleteOut(Schema):
    data: List[AddressAutocompleteItem]

class AddressOutOutagesItem(Schema):
    time: str
    date:str

class AddressOut(Schema):
    date: str
    full_address: str
    outages_flag: bool
    type: List[str]
    outages_ending: List[AddressOutOutagesItem]