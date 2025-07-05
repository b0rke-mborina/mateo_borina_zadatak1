from typing import Optional
import httpx
from aiocache import cached, SimpleMemoryCache
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import logging

from app.db.stats_orm import increment_statistic

logger = logging.getLogger(__name__)
BASE_URL = "https://dummyjson.com"

@cached(ttl=60, cache=SimpleMemoryCache)
async def get_all_dummyjson_tickets() -> list[dict]:
	logger.info("Fetching all tickets")
	async with httpx.AsyncClient() as client:
		resp = await client.get(f"{BASE_URL}/todos")
		resp.raise_for_status()
		resp_json = resp.json()
	async with httpx.AsyncClient() as client:
		params = {"skip": 0, "limit": resp_json["total"]}
		resp = await client.get(f"{BASE_URL}/todos", params=params)
		resp.raise_for_status()
		return resp.json()["todos"]

@cached(ttl=60, cache=SimpleMemoryCache)
async def get_dummyjson_tickets(skip: int, limit: int) -> list[dict]:
	logger.info(f"Fetching tickets with skip={skip} and limit={limit}")
	async with httpx.AsyncClient() as client:
		params = {"skip": skip, "limit": limit}
		resp = await client.get(f"{BASE_URL}/todos", params=params)
		resp.raise_for_status()
		return resp.json()

@cached(ttl=60, cache=SimpleMemoryCache)
async def get_dummyjson_ticket_by_id(ticket_id: int) -> dict:
	logger.info(f"Fetching ticket with ID: {ticket_id}")
	async with httpx.AsyncClient() as client:
		resp = await client.get(f"{BASE_URL}/todos/{ticket_id}")
		resp.raise_for_status()
		return resp.json()

@cached(ttl=60, cache=SimpleMemoryCache)
async def get_dummyjson_user(user_id: int, select: Optional[list[str]] = None) -> dict:
	logger.info(f"Fetching user with ID: {user_id}, select: {select}")
	async with httpx.AsyncClient() as client:
		params = {}
		if select:
			params['select'] = ','.join(select)
		resp = await client.get(f"{BASE_URL}/users/{user_id}", params=params)
		resp.raise_for_status()
		return resp.json()

async def post_dummyjson_login(username: str, password: str) -> dict:
	async with httpx.AsyncClient() as client:
		resp = await client.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password, "expiresInMins": 60})
		try:
			resp.raise_for_status()
			return resp.json()
		except httpx.HTTPStatusError:
			logger.error(f"Login failed with status code {resp.status_code}")
			increment_statistic("Total auth failures")
			if resp.status_code == 400:
				return {
					"status_code": 401,
					"error": "Invalid credentials",
				}
			else:
				logger.error(f"Unexpected error: {resp.text}")
				raise

async def post_dummyjson_authorization(auth_header: str) -> dict:
	async with httpx.AsyncClient() as client:
		response = await client.get(f"{BASE_URL}/auth/me", headers={"Authorization": auth_header})
		if response.status_code != 200:
			logger.error(f"Authorization failed with status code {response.status_code}")
			raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
		return response.json()
