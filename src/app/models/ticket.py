from pydantic import BaseModel

class Ticket(BaseModel):
	id: int
	title: str
	status: str
	priority: str
	assignee: str
	description: str

class TicketDetail(Ticket):
	id: int
	title: str
	status: str
	priority: str
	assignee: str
	description: str
	details: Ticket
