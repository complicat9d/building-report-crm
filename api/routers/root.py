from fastapi import Request, APIRouter, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from api.routes import templates
from database.dal import TokenDAL
from config import settings

router = APIRouter(include_in_schema=False)


@router.get(path="/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post(path="/", response_class=HTMLResponse)
async def authorise(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
):
    if login == settings.LOGIN and password == settings.PASSWORD:
        ip_address = request.client.host
        if not await TokenDAL.get_active(ip_address):
            await TokenDAL.create(ip_address)
        return RedirectResponse(url="/base", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
