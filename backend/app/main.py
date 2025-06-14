from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import health, users, plaid
from app.database import engine 
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal CFO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(health.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(plaid.router, prefix="/api")
