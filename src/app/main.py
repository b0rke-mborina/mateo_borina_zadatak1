from fastapi import FastAPI
from app.api.endpoints import tickets

app = FastAPI()

app.include_router(tickets.router)
