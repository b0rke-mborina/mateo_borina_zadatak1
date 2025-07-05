from app.models.ticket import Ticket

def calculate_priority(id: int) -> str:
	match id % 3:
		case 0: return "low"
		case 1: return "medium"
		case 2: return "high"

def map_to_ticket(todo: dict, user: dict) -> Ticket:
	return Ticket(
		id=todo["id"],
		title=todo["todo"],
		status="closed" if todo["completed"] else "open",
		priority=calculate_priority(todo["id"]),
		assignee=f"{user['firstName']} {user['lastName']}",
		description=todo["todo"][:100]
	)