from fastapi import APIRouter, UploadFile
from typing import Optional, List
from pathlib import Path

from database.dal import FileDAL
from schemas import FileSchema

router = APIRouter(prefix="/file", tags=["File"])


@router.post(path="/{report_id:int}", response_model=FileSchema)
async def create_file(file: UploadFile, report_id: int):
    contents = file.file.read()
    pwd = Path.cwd()
    new_filename = pwd / f"api/static/{file.filename}"
    with open(new_filename, "wb") as f:
        f.write(contents)

    file_id = await FileDAL.create(str(new_filename), report_id)
    return await FileDAL.get(file_id)


@router.get(path="/{report_id:int}", response_model=Optional[List[FileSchema]])
async def get_by_report_id(report_id: int):
    return await FileDAL.get_by_report_id(report_id)
