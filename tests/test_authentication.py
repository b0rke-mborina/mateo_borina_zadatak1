import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest.mock import patch, AsyncMock
from fastapi import status
from httpx import AsyncClient
from fastapi import FastAPI
from app.api.endpoints.authentication import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_login():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post("/login", json={"username": "user", "password": "pass"})
	
	assert response.status_code == status.HTTP_200_OK
