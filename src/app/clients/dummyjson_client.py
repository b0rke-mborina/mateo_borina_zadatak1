from typing import Optional
import httpx

BASE_URL = "https://dummyjson.com"

async def get_all_dummyjson_tickets() -> list[dict]:
	async with httpx.AsyncClient() as client:
		resp = await client.get(f"{BASE_URL}/todos")
		resp.raise_for_status()
		resp_json = resp.json()
	async with httpx.AsyncClient() as client:
		params = {"skip": 0, "limit": resp_json["total"]}
		resp = await client.get(f"{BASE_URL}/todos", params=params)
		resp.raise_for_status()
		return resp.json()["todos"]

async def get_dummyjson_tickets(skip: int, limit: int) -> list[dict]:
	async with httpx.AsyncClient() as client:
		params = {"skip": skip, "limit": limit}
		resp = await client.get(f"{BASE_URL}/todos", params=params)
		resp.raise_for_status()
		return resp.json()

async def get_dummyjson_ticket_by_id(ticket_id: int) -> dict:
	async with httpx.AsyncClient() as client:
		resp = await client.get(f"{BASE_URL}/todos/{ticket_id}")
		resp.raise_for_status()
		return resp.json()

async def get_dummyjson_user(user_id: int, select: Optional[list[str]] = None) -> dict:
	async with httpx.AsyncClient() as client:
		params = {}
		if select:
			params['select'] = ','.join(select)
		resp = await client.get(f"{BASE_URL}/users/{user_id}", params=params)
		resp.raise_for_status()
		return resp.json()
	
async def post_dummyjson_login(username: str, password: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
        resp.raise_for_status()
        return resp.json()