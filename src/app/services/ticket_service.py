from typing import List, Optional
from app.models.ticket import Ticket, TicketDetail
from typing import List
import asyncio
from app.clients.dummyjson_client import *
from app.utils.ticket_utils import calculate_priority, map_to_ticket
import logging

logger = logging.getLogger(__name__)
BASE_URL = "https://dummyjson.com/todos"

async def get_tickets(status: Optional[str], priority: Optional[str], skip: int, limit: int) -> dict:
	response = await get_dummyjson_tickets(skip=skip, limit=limit)
	todos = response["todos"]

	if status:
		todos = [t for t in todos if t["completed"] == (status == "closed")]
	if priority:
		todos = [t for t in todos if calculate_priority(t["id"]) == priority]

	user_ids = set(t["userId"] for t in todos)

	users = await asyncio.gather(
		*(get_dummyjson_user(user_id, select=["firstName", "lastName"]) for user_id in user_ids)
	)
	users = {user['id']: user for user in users}

	tickets = [map_to_ticket(todo, users[todo["userId"]]) for todo in todos]
	return {
		"tickets": tickets,
		"total": response["total"],
		"skip": skip,
		"limit": limit
	}

async def get_ticket_by_id(ticket_id: int) -> Optional[TicketDetail]:
	ticket = await get_dummyjson_ticket_by_id(ticket_id)
	user = await get_dummyjson_user(ticket["userId"], select=["firstName", "lastName"])
	ticket = map_to_ticket(ticket, user)
	if not ticket:
		logger.error(f"Ticket with ID {ticket_id} not found")
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

async def search_tickets(q: str) -> List[Ticket]:
	all_tickets = await get_all_dummyjson_tickets()
	filtered = [t for t in all_tickets if q.lower() in t['todo'].lower()]

	user_ids = set(t["userId"] for t in filtered)
	users = await asyncio.gather(
		*(get_dummyjson_user(user_id, select=["firstName", "lastName"]) for user_id in user_ids)
	)
	users = {user['id']: user for user in users}
	tickets = [map_to_ticket(todo, users[todo["userId"]]) for todo in filtered]

	return tickets
