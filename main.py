"""
Main entry point for the FastAPI application.
Defines the API routes and includes submodules for specific functionalities.
"""

from fastapi import FastAPI
from app.api import auth, record
from app.db.base import init_db
from app.services.random_gen_service import start_random_generator
from app.api.websocket import sio  # Import Socket.IO server
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp, AsyncServer
import asyncio

# Initialize FastAPI app
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
socket_app = ASGIApp(sio, other_asgi_app=fastapi_app)
app = socket_app  # Use the combined ASGI app
