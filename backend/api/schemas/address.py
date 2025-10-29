from ninja import Schema
from typing import List

class AddressAutocompleteItem(Schema):
    type:str
    address: str

class AddressAutocompleteOut(Schema):
    data: List[AddressAutocompleteItem]