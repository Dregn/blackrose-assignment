import random
import asyncio
from socketio import AsyncServer, ASGIApp
from app.services.auth_service import get_current_user  # Import your validation logic

# Initialize the Socket.IO server
sio = AsyncServer(async_mode="asgi")

@sio.event
async def connect(sid, environ):
    """
    Handles a new client connection and validates the Bearer token using the imported function.
    """
    headers = dict(environ["asgi.scope"].get("headers", []))
    auth_header = headers.get(b'authorization')

    if not auth_header:
        print(f"Missing authorization header for SID: {sid}")
        return False  # Deny the connection

    try:
        # Extract the token from the Authorization header
        token = auth_header.decode()
        print(f"Token received: {token}")

        # Use the imported function for validation
        user = get_current_user(token)
        print(f"Connection authorized for user: {user}")

        # Save user details in the session (await required)
        await sio.save_session(sid, {"user": user})
        return True  # Allow the connection

    except Exception as e:
        print(f"Authorization failed for SID: {sid}, Error: {e}")
        return False  # Deny the connection


@sio.event
async def disconnect(sid):
    """
    Handles a client disconnecting.
    """
    print(f"Client disconnected: {sid}")


@sio.on("ohlc-stream")
async def ohlc_stream(sid, data):
    """
    Streams random OHLC data to the client.
    """
    try:
        # Retrieve user details from the session (await required)
        session = await sio.get_session(sid)
        user = session.get("user")
        print(f"Streaming OHLC data for user: {user}")

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

            # Emit OHLC data to the client
            await sio.emit("ohlc-data", ohlc_data, room=sid)
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in OHLC stream for SID: {sid}, Error: {e}")


# Export the ASGI app
socket_app = ASGIApp(sio)
