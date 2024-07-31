from pydantic import BaseModel


class FileSchema(BaseModel):
    id: int
    path: str
    report_id: int
