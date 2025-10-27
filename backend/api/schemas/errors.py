from ninja import Schema
from typing import Optional

class ErrorSchema(Schema):
    message: str
    code: Optional[int] = None
    details: Optional[dict] = None