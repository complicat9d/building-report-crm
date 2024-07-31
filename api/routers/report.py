from fastapi import APIRouter
from typing import List, Optional

from database.dal import ReportDAL
from schemas import ReportSchema, ReportCreationRequest

router = APIRouter(prefix="/report", tags=["Report"])


@router.post(path="", response_model=Optional[ReportSchema])
async def create_report(request: ReportCreationRequest):
    report_id = await ReportDAL.create(**request.model_dump())
    return await ReportDAL.get(report_id)


@router.get(path="/{employee_id:int}", response_model=Optional[List[ReportSchema]])
async def get_report_by_employee_id(employee_id: int):
    return await ReportDAL.get_by_employee_id(employee_id)


@router.get(path="/{facility_id:int}", response_model=Optional[List[ReportSchema]])
async def get_report_by_facility_id(facility_id: int):
    return await ReportDAL.get_by_facility_id(facility_id)
