from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.models.ticket import Ticket, TicketDetail
from app.services.ticket_service import get_tickets, get_ticket_by_id, search_tickets

router = APIRouter()

@router.get("/tickets", response_model=List[Ticket])
async def read_tickets(status: Optional[str] = Query(None), priority: Optional[str] = Query(None), page: int = 0, limit: int = 10):
	return await get_tickets(status=status, priority=priority, page=page, limit=limit)

@router.get("/tickets/search", response_model=List[Ticket])
async def search(q: str = Query(...), page: int = 0, limit: int = 10):
	return await search_tickets(q, page, limit)

@router.get("/tickets/{ticket_id}", response_model=TicketDetail)
async def read_ticket(ticket_id: int):
	ticket = await get_ticket_by_id(ticket_id)
	if not ticket:
		raise HTTPException(status_code=404, detail="Ticket not found")
	return ticket
