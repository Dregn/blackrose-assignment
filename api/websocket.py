import random
import asyncio
from fastapi import APIRouter, WebSocket, Depends, HTTPException
from .services.auth_service import get_current_user

router = APIRouter()

MAX_CONNECTIONS = 100
active_connections = []


@router.websocket("/ohlc-stream/")
async def websocket_ohlc_stream(websocket: WebSocket,username=Depends(get_current_user)):
    """
    Streams random OHLC data continuously for WebSocket clients.
    """
    await websocket.accept()

    try:
        print("New connection established.")
        current_price = random.uniform(100, 200)

        while True:
            open_price = current_price
            high_price = open_price + random.uniform(0.1, 5)
            low_price = open_price - random.uniform(0.1, 5)
            close_price = random.uniform(low_price, high_price)
            current_price = close_price

            ohlc_data = {
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
            }

            await websocket.send_json(ohlc_data)
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
    finally:
        print("WebSocket connection closed.")
        await websocket.close()