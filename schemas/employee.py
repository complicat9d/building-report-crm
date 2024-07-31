from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class EmployeeSchema(BaseModel):
    id: int
    chat_id: Optional[int] = None
    fio: str
    job_title: Optional[str] = None
    token: UUID
    is_active: bool


class EmployeeCreationRequest(BaseModel):
    fio: str
    job_title: str
    facilities: Optional[List[int]]


class EmployeeUpdateRequest(BaseModel):
    id: int
    fio: Optional[str] = None
    job_title: Optional[str] = None
    is_active: Optional[bool] = None
    facilities: Optional[List[int]] = []


class EmployeeActivateRequest(BaseModel):
    chat_id: int
    token: UUID
