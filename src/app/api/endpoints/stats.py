from fastapi import APIRouter, Request
from app.db.stats_orm import increment_statistic, get_all_statistics
from app.utils.request_limiter import limiter

router = APIRouter()

@router.get("/stats", response_model=dict)
@limiter.limit("10/minute")
def stats(request: Request):
	increment_statistic(["Total requests to /stats", "Total requests"])
	return get_all_statistics()