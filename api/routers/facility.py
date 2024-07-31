from fastapi import APIRouter
from starlette import status
from typing import List, Optional


from database.dal import FacilityDAL
from schemas import (
    FacilitySchema,
    FacilityCreationRequest,
    FacilityUpdateRequest,
    FacilityUpdateActiveRequest,
)

router = APIRouter(prefix="/facility", tags=["Facility"])


@router.get(path="", response_model=Optional[List[FacilitySchema]])
async def get_all_facilities():
    return await FacilityDAL.get_all()


@router.post(path="", status_code=status.HTTP_200_OK)
async def create_facility(request: FacilityCreationRequest):
    await FacilityDAL.create(**request.model_dump())


@router.put(path="", status_code=status.HTTP_200_OK)
async def update_facility(request: FacilityUpdateRequest):
    await FacilityDAL.update(**request.model_dump())


@router.put(path="/active", status_code=status.HTTP_200_OK)
async def update_active_facility(request: FacilityUpdateActiveRequest):
    await FacilityDAL.update(**request.model_dump())


@router.delete(path="/{id:int}", status_code=status.HTTP_200_OK)
async def delete_facility(id: int):
    await FacilityDAL.delete(id)


@router.get(path="/{id:int}", response_model=Optional[FacilitySchema])
async def get_facility_by_id(id: int):
    return await FacilityDAL.get(id)


@router.get(path="/{employee_id:int}", response_model=Optional[List[FacilitySchema]])
async def get_employee_facilities(employee_id: int):
    return await FacilityDAL.get_all_by_employee_id(employee_id)
