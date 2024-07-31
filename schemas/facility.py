from pydantic import BaseModel
from typing import List, Optional


class FacilitySchema(BaseModel):
    id: int
    title: str
    description: str
    address: str
    active: bool = False


class FacilityCreationRequest(BaseModel):
    title: str
    description: str
    active: bool
    address: str
    employees: List[int] = None


class FacilityUpdateRequest(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    address: Optional[str] = None
    employees: Optional[List[int]] = None


class FacilityUpdateActiveRequest(BaseModel):
    id: int
    active: bool


class FacilityPaginated(BaseModel):
    items: List[FacilitySchema] = []
    total: int
    page: int
    pages: int
    prev_num: Optional[int]
    next_num: Optional[int]
    has_prev: bool
    has_next: bool
