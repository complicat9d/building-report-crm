from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Response, Request

from api.routes import router as routes
from api.routers.root import router as root_router
from api.routers.file import router as file_router
from api.routers.report import router as report_router
from api.routers.employee import router as employee_router
from api.routers.facility import router as facility_router
from config import settings

app = FastAPI()

app.mount("/api/static", StaticFiles(directory="api/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback

    return Response(
        content="".join(
            traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
        )
    )


app.include_router(root_router)

router = APIRouter(prefix="/api", include_in_schema=settings.ENABLE_DOCS)
router.include_router(employee_router)
router.include_router(report_router)
router.include_router(file_router)
router.include_router(facility_router)

app.include_router(routes)
app.include_router(router)
