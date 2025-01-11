"""
Service for generating random numbers and saving them to the database.
"""

import asyncio
import random
from datetime import datetime
from app.db.random_repo import save_random_number

async def start_random_generator():
    """
    Continuously generates random numbers every second and saves them to the database.
    """
    while True:
        timestamp = datetime.now().isoformat()
        value = random.randint(1, 100)
        save_random_number(timestamp, value)
        await asyncio.sleep(1)
