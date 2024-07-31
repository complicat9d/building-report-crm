from typing import List
from datetime import timedelta
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request, APIRouter, Form, UploadFile, status

from database.dal import (
    EmployeeDAL,
    FacilityDAL,
    ReportDAL,
    PauseDAL,
    FileDAL,
    FacilityEmployeeDAL,
)
from schemas import (
    EmployeeNotFoundException,
    FacilityNotFoundException,
    ReportHTMLResponse,
)
from middleware import EmployeeMiddleware
from utils import paginate, zulu_to_gmt, auth_dep
from config import settings

router = APIRouter(include_in_schema=False, dependencies=[auth_dep])
templates = Jinja2Templates(directory="api/templates")


@router.get(path="/base", response_class=HTMLResponse)
async def authorise(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get(path="/employees", response_class=HTMLResponse)
async def show_employees(request: Request, page: int = 1, per_page: int = 10):
    employees = await EmployeeDAL.get_all()

    total_pages, paginated_employees = paginate(employees, page, per_page)

    return templates.TemplateResponse(
        "employees.html",
        {
            "request": request,
            "employees": paginated_employees,
            "current_page": page,
            "pages": total_pages,
            "bot_name": settings.BOT_NAME,
        },
    )


@router.get(path="/employees/create", response_class=HTMLResponse)
async def get_create_employee(request: Request):
    return templates.TemplateResponse("employee_create.html", {"request": request})


@router.post(path="/employees/create", response_class=HTMLResponse)
async def post_create_employee(
    request: Request,
    fio: str = Form(...),
    job_title: str = Form(...),
    facilities: List[int] = Form(default=[]),
):
    employee_id = await EmployeeMiddleware.create(fio, job_title, facilities)
    return RedirectResponse(
        url=f"/employees/{employee_id}/profile", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(path="/employees/{id}/profile", response_class=HTMLResponse)
async def get_employee_profile(request: Request, id: int):
    result = []
    facilities = await FacilityDAL.get_all_by_employee_id(id)
    employee = await EmployeeDAL.get_by_id(id)
    reports = await ReportDAL.get_by_employee_id(id)

    for report in reports:

        address = (await FacilityDAL.get(report.facility_id)).address
        files = await FileDAL.get_by_report_id(report.id)
        paths = [file.path.split("/")[-1] for file in files]

        shift_start = zulu_to_gmt(report.shift_start)
        shift_end = zulu_to_gmt(report.shift_end)
        total_time = (
            await PauseDAL.get_break_time(report.id)
            + report.shift_end
            - report.shift_start
        )
        result.append(
            ReportHTMLResponse(
                id=report.id,
                title=report.title,
                description=report.description,
                shift_start=shift_start,
                shift_end=shift_end,
                total_time=total_time - timedelta(microseconds=total_time.microseconds),
                facility_address=address,
                files=paths,
            )
        )

    return templates.TemplateResponse(
        "employee_profile.html",
        {
            "request": request,
            "employee": employee,
            "facilities": facilities,
            "reports": result,
            "bot_name": settings.BOT_NAME,
        },
    )


@router.get(path="/employees/{id}/update", response_class=HTMLResponse)
async def get_update_employee(request: Request, id: int):
    employee = await EmployeeDAL.get_by_id(id)
    if not employee:
        raise EmployeeNotFoundException

    facilities = await FacilityDAL.get_all()
    employee_facilities = await FacilityDAL.get_all_by_employee_id(id)
    employee_facility_ids = [facility.id for facility in employee_facilities]

    for facility in facilities:
        facility.active = facility.id in employee_facility_ids

    return templates.TemplateResponse(
        "employee_update.html",
        {
            "request": request,
            "user": employee,
            "places": facilities,
        },
    )


@router.post(path="/employees/{id}/update", response_class=HTMLResponse)
async def post_update_employee(
    request: Request,
    id: int,
    fio: str = Form(...),
    job_title: str = Form(...),
    is_active: bool = Form(...),
    facilities: List[int] = Form(default=[]),
):
    employee = await EmployeeDAL.get_by_id(id)
    if not employee:
        raise EmployeeNotFoundException

    await EmployeeDAL.update(id=id, fio=fio, job_title=job_title, is_active=is_active)

    curr_employee_facilities = await FacilityDAL.get_all_by_employee_id(employee.id)
    # delete all the current relationships employee has
    for facility in curr_employee_facilities:
        await FacilityEmployeeDAL.delete(facility.id, id)

    # create all the new relationships
    for facility_id in facilities:
        await FacilityEmployeeDAL.create(facility_id, id)

    facilities = await FacilityDAL.get_all()
    employee_facilities = await FacilityDAL.get_all_by_employee_id(id)
    employee_facility_ids = [facility.id for facility in employee_facilities]

    for facility in facilities:
        facility.active = facility.id in employee_facility_ids

    return templates.TemplateResponse(
        "employee_update.html",
        {
            "request": request,
            "user": employee,
            "places": facilities,
        },
    )


@router.delete(path="/employees/delete/{id}")
async def delete_employee(request: Request, id: int):
    await EmployeeDAL.delete(id)
    return RedirectResponse("/employees", status_code=status.HTTP_303_SEE_OTHER)


@router.get(path="/facilities/", response_class=HTMLResponse)
async def show_facilities(request: Request, page: int = 1, per_page: int = 10):
    facilities = await FacilityDAL.get_all()
    total_pages, paginated_facilities = paginate(facilities, page, per_page)

    return templates.TemplateResponse(
        "facilities.html",
        {
            "request": request,
            "facilities": paginated_facilities,
            "current_page": page,
            "pages": total_pages,
        },
    )


@router.get(path="/facilities/create", response_class=HTMLResponse)
async def get_create_facility(request: Request):
    employees = await EmployeeDAL.get_all()
    return templates.TemplateResponse(
        "facility_create.html",
        {
            "request": request,
            "employees": employees,
        },
    )


@router.post(path="/facilities/create", response_class=HTMLResponse)
async def post_create_facility(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    active: bool = Form(True),
    address: str = Form(...),
    employees: List[int] = Form(default=[]),
):
    facility_id = await FacilityDAL.create(
        title=title,
        description=description,
        active=active,
        address=address,
        employees=employees,
    )

    return RedirectResponse(
        url=f"/facilities/{facility_id}/profile", status_code=status.HTTP_303_SEE_OTHER
    )


@router.get(path="/facilities/{facility_id}/profile", response_class=HTMLResponse)
async def show_facility_details(request: Request, facility_id: int):
    result = []

    facility = await FacilityDAL.get(facility_id)
    if not facility:
        raise FacilityNotFoundException

    employees = await EmployeeDAL.get_all_by_facility_id(facility_id)
    reports = await ReportDAL.get_by_facility_id(facility_id)

    for report in reports:
        files = await FileDAL.get_by_report_id(report.id)
        paths = [file.path.split("/")[-1] for file in files]

        shift_start = zulu_to_gmt(report.shift_start)
        shift_end = zulu_to_gmt(report.shift_end)
        total_time = (
            await PauseDAL.get_break_time(report.id)
            + report.shift_end
            - report.shift_start
        )
        res = ReportHTMLResponse(
            id=report.id,
            title=report.title,
            description=report.description,
            shift_start=shift_start,
            shift_end=shift_end,
            total_time=total_time - timedelta(microseconds=total_time.microseconds),
            facility_address=facility.address,
            files=paths,
        )
        result.append(res)

    for employee in employees:
        employee.is_active = True

    return templates.TemplateResponse(
        "facility_profile.html",
        {
            "request": request,
            "facility": facility,
            "employees": employees,
            "reports": result,
        },
    )


@router.get(path="/facilities/{facility_id}/update/", response_class=HTMLResponse)
async def get_update_facility(request: Request, facility_id: int):
    facility = await FacilityDAL.get(facility_id)
    if not facility:
        raise FacilityNotFoundException

    employees = await EmployeeDAL.get_all()
    facility_employees = await EmployeeDAL.get_all_by_facility_id(facility_id)
    facility_employee_ids = [employee.id for employee in facility_employees]

    for employee in employees:
        employee.is_active = employee.id in facility_employee_ids

    return templates.TemplateResponse(
        "facility_update.html",
        {
            "request": request,
            "facility": facility,
            "employees": employees,
        },
    )


@router.post(path="/facilities/{facility_id}/update/", response_class=HTMLResponse)
async def post_update_facility(
    request: Request,
    facility_id: int,
    title: str = Form(...),
    description: str = Form(...),
    active: bool = Form(...),
    address: str = Form(...),
    employees: List[int] = Form(default=[]),
):
    facility = await FacilityDAL.get(facility_id)
    if not facility:
        raise FacilityNotFoundException

    await FacilityDAL.update(
        id=facility_id,
        description=description,
        title=title,
        active=active,
        address=address,
        employees=employees,
    )

    employees = await EmployeeDAL.get_all()
    facility_employees = await EmployeeDAL.get_all_by_facility_id(facility_id)
    facility_employee_ids = [employee.id for employee in facility_employees]

    for employee in employees:
        employee.is_active = employee.id in facility_employee_ids

    return templates.TemplateResponse(
        "facility_update.html",
        {
            "request": request,
            "facility": facility,
            "employees": employees,
        },
    )


@router.delete(path="/facilities/{id}/delete")
async def delete_facility(request: Request, id: int):
    await FacilityDAL.delete(id)
    return RedirectResponse(url="/facilities/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/file/upload/", response_class=HTMLResponse)
async def upload_file(
    request: Request, file: UploadFile = Form(...), report_id: int = Form(...)
):
    return {"filename": file.filename, "report_id": report_id}
