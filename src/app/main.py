from fastapi import FastAPI
from app.api.endpoints import tickets, authentication

app = FastAPI()

app.include_router(tickets.router)
app.include_router(authentication.router)
