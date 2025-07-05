from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

def key_function(request: Request) -> str:
	if 'Authorization ' in request.headers:
		return request.headers['Authorization'].split()[1]
	return get_remote_address(request)

limiter = Limiter(key_func=key_function)
