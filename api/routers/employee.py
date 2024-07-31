from fastapi import APIRouter
from starlette import status
from typing import List, Optional

from database.dal import EmployeeDAL, FacilityEmployeeDAL
from schemas import (
    EmployeeCreationRequest,
    EmployeeUpdateRequest,
    EmployeeActivateRequest,
    EmployeeSchema,
)
from middleware.employee import EmployeeMiddleware


router = APIRouter(prefix="/employee", tags=["Employee"])


@router.get(path="", response_model=Optional[List[EmployeeSchema]])
async def get_all_employees():
    return await EmployeeDAL.get_all()


@router.post(path="", response_model=EmployeeSchema)
async def create_employee(request: EmployeeCreationRequest):
    employee_id = await EmployeeMiddleware.create(**request.model_dump())
    return await EmployeeDAL.get_by_id(employee_id)


@router.put(path="", status_code=status.HTTP_200_OK)
async def update_employee(request: EmployeeUpdateRequest):
    await EmployeeDAL.update(
        id=request.id,
        fio=request.fio,
        job_title=request.job_title,
        is_active=request.is_active,
    )
    for facility_id in request.facilities:
        await FacilityEmployeeDAL.create(facility_id, request.id)


@router.put(path="/activate", status_code=status.HTTP_200_OK)
async def activate_employee(request: EmployeeActivateRequest):
    await EmployeeDAL.activate(**request.model_dump())


@router.delete(path="/{id:int}", status_code=status.HTTP_200_OK)
async def delete_employee(id: int):
    await EmployeeDAL.delete(id)


@router.get(path="/{id:int}", response_model=Optional[EmployeeSchema])
async def get_employee_by_id(id: int):
    return await EmployeeDAL.get_by_id(id)


@router.get(path="/{chat_id:int}", response_model=Optional[EmployeeSchema])
async def get_employee_by_chat_id(chat_id: int):
    return await EmployeeDAL.get_by_chat_id(chat_id)


@router.get(path="/{facility_id:int}", response_model=Optional[List[EmployeeSchema]])
async def get_employee_by_facility_id(facility_id: int):
    return await EmployeeDAL.get_all_by_facility_id(facility_id)
