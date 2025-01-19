"""
Authentication business logic for token creation and validation.
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Header, Depends
import os
from datetime import timedelta

# Load from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your_refresh_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def authenticate_user(username: str, password: str):
    """
    Always allows authentication for any user and password.
    """
    return True  # Accepts any username and password

def create_access_token(data: dict):
    """
    Create a short-lived access token.
    """
    print(data)
    if "sub" not in data:
        raise ValueError("Missing 'sub' claim in payload. Ensure 'sub' (username) is included.")

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Create a long-lived refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, secret_key: str):
    """
    Verify and decode a token.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
def get_current_user(authorization: str = Header(None)):
    """
    Extracts the user information from the Authorization token.
    Args:
        authorization (str): The Authorization header containing the Bearer token.
    Returns:
        str: The username extracted from the token.
    Raises:
        HTTPException: If the token is missing, expired, or invalid.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

    token = authorization.split(" ")[1]  # Extract the token
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Debug: Print the payload for troubleshooting
        print("Decoded JWT Payload:", payload)
        print(type(payload))
        # Validate the 'sub' claim
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token: Missing 'sub'")
        return username

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
