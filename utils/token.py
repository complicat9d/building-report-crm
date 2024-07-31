from fastapi import Depends, Request, status, HTTPException
from datetime import datetime, timedelta, timezone

from database.dal import TokenDAL


async def _check_authorisation(request: Request):
    ip_address = request.client.host
    active = await TokenDAL.get_active(ip_address)

    if not active:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/"}
        )
    else:
        now = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=3)
        if active.expires < now:
            await TokenDAL.update(ip_address, is_expired=True)
            raise HTTPException(
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                headers={"Location": "/"},
            )
        else:
            await TokenDAL.update(ip_address, time_increment=timedelta(minutes=1))


auth_dep = Depends(_check_authorisation)
