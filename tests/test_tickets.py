import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest.mock import patch, AsyncMock
from fastapi import status
from httpx import AsyncClient
from fastapi import FastAPI
from app.api.endpoints.tickets import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
@patch("app.services.ticket_service.get_tickets", new_callable=AsyncMock)
async def test_read_tickets(mock_get_tickets):
	mock_get_tickets.return_value = {"data": "some tickets"}

	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/tickets?status=open&priority=high&skip=0&limit=5")
	
	assert response.status_code == status.HTTP_200_OK
	assert "tickets" in response.json()
	assert "limit" in response.json()
	assert "skip" in response.json()
	assert "total" in response.json()


@pytest.mark.asyncio
@patch("app.services.ticket_service.search_tickets", new_callable=AsyncMock)
async def test_search_tickets(mock_search_tickets):
	mock_search_tickets.return_value = [{"id": 1, "title": "test ticket"}]
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/tickets/search?q=test")
	assert response.status_code == status.HTTP_200_OK
	assert isinstance(response.json(), list)


@pytest.mark.asyncio
@patch("app.services.ticket_service.get_ticket_by_id", new_callable=AsyncMock)
async def test_read_ticket_found(mock_get_ticket):
	mock_get_ticket.return_value = {"id": 1, "title": "Found ticket"}
	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/tickets/1")
	assert response.status_code == status.HTTP_200_OK
	assert response.json()["id"] == 1


@pytest.mark.asyncio
@patch("app.services.ticket_service.get_ticket_by_id", new_callable=AsyncMock)
async def test_read_ticket_not_found(mock_get_ticket):
	mock_get_ticket.return_value = None

	async with AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/tickets/3")
	
	assert response.status_code == status.HTTP_200_OK
	assert "id" in response.json()
	assert "title" in response.json()
	assert "status" in response.json()
	assert "priority" in response.json()
	assert "assignee" in response.json()
	assert "description" in response.json()
	assert "details" in response.json()
