from fastapi import APIRouter
from app.db.stats_orm import increment_statistic, get_all_statistics
from app.services.auth_service import user_login
from app.models.login import LoginRequest

router = APIRouter()

@router.get("/stats")
def stats():
	increment_statistic(["Total requests to /stats", "Total requests"])
	return get_all_statistics()