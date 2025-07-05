from fastapi import Request, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
import httpx

async def auth_required(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/auth/me", headers={"Authorization": auth_header})
        if response.status_code != 200:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = response.json()

    request.state.user = user