"""
Main entry point for the FastAPI application.
Defines the API routes and includes submodules for specific functionalities.
"""

from fastapi import FastAPI
from app.api import auth, record, websocket
from app.db.base import init_db
import asyncio
from app.services.random_gen_service import start_random_generator
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI(title="Black Rose Assignment", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],  # Allowed origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Initialize the database on application startup
@app.on_event("startup")
def initialize_database():
    init_db()

# Start the random number generator as a background task
@app.on_event("startup")
async def start_services():
    asyncio.create_task(start_random_generator())

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(record.router, prefix="/record", tags=["CRUD Operations"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
