from pydantic import BaseModel
from datetime import datetime


class TokenSchema(BaseModel):
    id: int
    ip_address: str
    expires: datetime
    is_expired: bool
