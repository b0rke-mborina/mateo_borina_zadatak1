from fastapi import APIRouter, Query, HTTPException, Depends, Request
from typing import List, Optional
from app.db.stats_orm import increment_statistic
from app.models.ticket import Ticket, TicketDetail
from app.services.ticket_service import get_tickets, get_ticket_by_id, search_tickets
from app.core.middlewares import auth_required
from app.utils.request_limiter import limiter
import logging

# Disabled this for development
# router = APIRouter(dependencies=[Depends(auth_required)])
router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/tickets", response_model=dict)
@limiter.limit("10/minute")
async def read_tickets(request: Request, status: Optional[str] = Query(None), priority: Optional[str] = Query(None), skip: int = 0, limit: int = 10):
	logger.info(f"Request received: status={status}, priority={priority}, skip={skip}, limit={limit}")
	increment_statistic(["Total requests to /tickets*", "Total requests"])
	
	return await get_tickets(status=status, priority=priority, skip=skip, limit=limit)

@router.get("/tickets/search", response_model=List[Ticket])
@limiter.limit("5/minute")
async def search(request: Request, q: str = Query(...)):
	logger.info(f"Search request received: {q}")
	increment_statistic(["Total requests to /tickets*", "Total requests"])

	return await search_tickets(q)

@router.get("/tickets/{ticket_id}", response_model=TicketDetail)
@limiter.limit("5/second")
async def read_ticket(request: Request, ticket_id: int):
	logger.info(f"Request received for ticket ID: {ticket_id}")
	increment_statistic(["Total requests to /tickets*", "Total requests"])

	ticket = await get_ticket_by_id(ticket_id)
	if not ticket:
		logger.error(f"Ticket with ID {ticket_id} not found")
		raise HTTPException(status_code=404, detail="Ticket not found")
	return ticket
