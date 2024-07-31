from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PauseSchema(BaseModel):
    id: int
    start: datetime
    end: Optional[datetime] = None
    report_id: int
