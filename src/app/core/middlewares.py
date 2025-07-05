from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from app.clients.dummyjson_client import post_dummyjson_authorization
import logging

logger = logging.getLogger(__name__)

async def auth_required(request: Request):
	auth_header = request.headers.get("Authorization")
	if not auth_header:
		logger.warning("Authorization header missing")
		raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

	user = await post_dummyjson_authorization(auth_header)

	request.state.user = user