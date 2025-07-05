from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.endpoints import tickets, authentication, stats
from app.utils.request_limiter import limiter
import logging
from app.logging.logging_config import setup_logging
from app.db import stats_orm

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(tickets.router)
app.include_router(authentication.router)
app.include_router(stats.router)

stats_orm.init_db()
stats_orm.seed_statistics()

setup_logging()
logger = logging.getLogger(__name__)

logger.info("App started")
