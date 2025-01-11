"""
Main entry point for the FastAPI application.
Defines the API routes and includes submodules for specific functionalities.
"""

from fastapi import FastAPI
from .api import auth, record, websocket
from .db.base import init_db
import asyncio
from .services.random_gen_service import start_random_generator

app = FastAPI(title="Enterprise-Grade Full-Stack Backend", version="1.0.0")

# Initialize the database on application startup
@.on_event("startup")
def initialize_database():
    init_db()

# Start the random number generator as a background task
@.on_event("startup")
async def start_services():
    asyncio.create_task(start_random_generator())

# Include API routes
.include_router(auth.router, prefix="/auth", tags=["Authentication"])
.include_router(record.router, prefix="/record", tags=["CRUD Operations"])
.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
