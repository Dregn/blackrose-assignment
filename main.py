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
from socketio import ASGIApp
import asyncio

# Initialize FastAPI
app = FastAPI(title="Black Rose Assignment", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],  # Allow localhost origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allow localhost in Socket.IO
sio = sio.AsyncServer(cors_allowed_origins=["http://localhost", "http://localhost:3000"])  # Configure CORS for Socket.IO

# Initialize database
@app.on_event("startup")
def initialize_database():
    init_db()

# Start background services
@app.on_event("startup")
async def start_services():
    asyncio.create_task(start_random_generator())

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(record.router, prefix="/record", tags=["CRUD Operations"])

# Combine FastAPI and Socket.IO apps
socket_app = ASGIApp(sio, other_asgi_app=app)
app = socket_app  # Assign the combined ASGI app to `app`
