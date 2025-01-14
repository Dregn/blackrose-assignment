"""
Main entry point for the FastAPI application.
Defines the API routes and includes submodules for specific functionalities.
"""

from fastapi import FastAPI
from app.api import auth, record
from app.db.base import init_db
from app.services.random_gen_service import start_random_generator
from app.api.websocket import socket_app  # Import ASGI Socket.IO app
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Initialize FastAPI
fastapi_app = FastAPI(title="Black Rose Assignment", version="1.0.0")

# Configure CORS for FastAPI
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],  # Allow localhost origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@fastapi_app.on_event("startup")
def initialize_database():
    init_db()

# Start background services
@fastapi_app.on_event("startup")
async def start_services():
    asyncio.create_task(start_random_generator())

# Include API routes
fastapi_app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
fastapi_app.include_router(record.router, prefix="/record", tags=["CRUD Operations"])

# Combine FastAPI and Socket.IO apps
app = socket_app  # ASGI combined app from `api/websocket.py`
