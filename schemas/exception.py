from fastapi import HTTPException
from starlette import status

EmployeeNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
)

FacilityNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Facility not found"
)

PauseNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Pause not found"
)

FileNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
)

EmployeeAlreadyActivatedException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Employee is already activated"
)

ReportNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Report not found"
)

TokenNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Token for this ip-address not found"
)

MessageNotFoundException = Exception("Message not found")

PhotoLimitExceededException = Exception("Photo limit for one report exceeded")
