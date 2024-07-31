from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List


class ReportSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    shift_start: datetime
    shift_end: Optional[datetime] = None
    employee_id: int
    facility_id: int


class ReportCreationRequest(BaseModel):
    title: str
    employee_id: int
    facility_id: int
    shift_start: datetime


class ReportHTMLResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    shift_start: datetime
    shift_end: datetime
    total_time: timedelta
    facility_address: str = None
    employee_fio: str = None
    files: Optional[List[str]] = None
