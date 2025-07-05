from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
from app.models.ticket import Ticket, TicketDetail
from app.services.ticket_service import get_tickets, get_ticket_by_id, search_tickets
from app.middlewares import auth_required

# Disabled this for development
# router = APIRouter(dependencies=[Depends(auth_required)])
router = APIRouter()
    
@router.get("/tickets", response_model=dict)
async def read_tickets(status: Optional[str] = Query(None), priority: Optional[str] = Query(None), skip: int = 0, limit: int = 10):
	return await get_tickets(status=status, priority=priority, skip=skip, limit=limit)

@router.get("/tickets/search", response_model=List[Ticket])
async def search(q: str = Query(...)):
	return await search_tickets(q)

@router.get("/tickets/{ticket_id}", response_model=TicketDetail)
async def read_ticket(ticket_id: int):
	ticket = await get_ticket_by_id(ticket_id)
	if not ticket:
		raise HTTPException(status_code=404, detail="Ticket not found")
	return ticket
