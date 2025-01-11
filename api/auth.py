"""
Authentication API endpoints.
Handles user login and session token generation.
"""
import  os
from fastapi import APIRouter, Depends,HTTPException
from fastapi.responses import JSONResponse
from .models.auth import LoginRequest, TokenResponse
from .services.auth_service import authenticate_user, create_access_token,create_refresh_token,verify_token

router = APIRouter()
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your_refresh_secret_key")
@router.post("/login", response_model=TokenResponse, summary="User login endpoint")
def login(credentials: LoginRequest):
    """
    Validates user credentials and returns a session token.
    """
    if not authenticate_user(credentials.username, credentials.password):
        return JSONResponse(status_code=401, content={"message": "Invalid username or password"})

    access_token = create_access_token({
    "sub": credentials.username,
    "password": credentials.password
})
    refresh_token = create_refresh_token({
    "sub": credentials.username,
    "password": credentials.password
})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    """
    Refresh the access token using a valid refresh token.
    """
    payload = verify_token(refresh_token, REFRESH_SECRET_KEY)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": username})
    new_refresh_token = create_refresh_token({"sub": username})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

