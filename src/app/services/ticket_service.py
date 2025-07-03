from typing import List, Optional
from app.models.ticket import Ticket, TicketDetail
import httpx
from typing import List

BASE_URL = "https://dummyjson.com/todos"

async def get_all_tickets() -> list[Ticket]:
	raw_todos = await get_dummyjson_tickets()
	tickets = []
	for todo in raw_todos:
		ticket = await map_to_ticket(todo)
		tickets.append(ticket)
	return tickets

"""async def get_all_tickets() -> List[Ticket]:
	tickets = []
	limit = 100
	skip = 0
	total = None

	async with httpx.AsyncClient() as client:
		while total is None or skip < total:
			response = await client.get(f"{BASE_URL}?limit={limit}&skip={skip}")
			response.raise_for_status()
			data = response.json()

			total = data.get("total", 0)
			todos = data.get("todos", [])
			tickets.extend(Ticket(**todo) for todo in todos)

			skip += limit

	return tickets"""

def paginate(items, page: int = 0, limit: int = 10):
	start = (page - 1) * limit
	end = start + limit
	return items[start:end]

async def get_tickets(status: Optional[str], priority: Optional[str], page: int, limit: int) -> List[Ticket]:
	filtered = await get_all_tickets()
	if status:
		filtered = [t for t in filtered if t.status == status]
	if priority:
		filtered = [t for t in filtered if t.priority == priority]
	return [
		Ticket(
			id=t.id,
			title=t.title,
			status=t.status,
			priority=t.priority,
			description=t.description[:100],
			assignee=t.assignee
		)
		for t in paginate(filtered, page, limit)
	]

async def get_ticket_by_id(ticket_id: int) -> Optional[TicketDetail]:
	ticket = next((t for t in await get_all_tickets() if t.id == ticket_id), None)
	if not ticket:
		return None
	return TicketDetail(
		id=ticket.id,
		title=ticket.title,
		status=ticket.status,
		priority=ticket.priority,
		description=ticket.description[:100],
		assignee=ticket.assignee,
		details=ticket
	)

async def search_tickets(q: str, page: int, limit: int) -> List[Ticket]:
	filtered = [t for t in await get_all_tickets() if q.lower() in t.title.lower()]
	return [
		Ticket(
			id=t.id,
			title=t.title,
			status=t.status,
			priority=t.priority,
			description=t.description[:100],
			assignee=t.assignee
		)
		for t in paginate(filtered, page, limit)
	]

async def get_dummyjson_tickets() -> list[dict]:
	async with httpx.AsyncClient() as client:
		resp = await client.get("https://dummyjson.com/todos")
		resp.raise_for_status()
		return resp.json()["todos"]

async def get_dummyjson_user(user_id: int) -> dict:
	async with httpx.AsyncClient() as client:
		resp = await client.get(f"https://dummyjson.com/users/{user_id}")
		resp.raise_for_status()
		return resp.json()

def calculate_priority(id: int) -> str:
	match id % 3:
		case 0: return "low"
		case 1: return "medium"
		case 2: return "high"

async def map_to_ticket(todo: dict) -> Ticket:
	user = await get_dummyjson_user(todo["userId"])
	return Ticket(
		id=todo["id"],
		title=todo["todo"],
		status="closed" if todo["completed"] else "open",
		priority=calculate_priority(todo["id"]),
		assignee=f"{user['firstName']} {user['lastName']}",
		description=todo["todo"][:100]
	)
