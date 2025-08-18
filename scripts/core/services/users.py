from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scripts.core.schemas.users import RegisterUser
from scripts.core.handler.user import UserHandler
from scripts.db.pg.sessions import get_db

user_router = APIRouter(prefix="/users", tags=["Users"], redirect_slashes=True)

@user_router.post("/register", summary="Register a new user")
async def register_user(register_data: RegisterUser, session: AsyncSession = Depends(get_db)):
    """
    Endpoint to register a new user.
    This endpoint will handle user registration logic.
    """
    return await UserHandler(session=session).register_user(register_data=register_data)



@user_router.post("/login", summary="User login")
async def login_user():
    """
    Endpoint for user login.
    This endpoint will handle user authentication and return a token.
    """
    return {"message": "User login endpoint"}

@user_router.put("/verify-email/{verification_token}", summary="Verify user email")
async def verify_email(verification_token: str):
    """
    Endpoint to verify user email using a verification token.

    Args:
        verification_token (str): The token used for email verification.

    Returns:
        dict: Confirmation message of email verification.
    """
    return {"verification_token": verification_token, "message": "Email verified successfully"}

@user_router.post("/request-password-reset", summary="Request password reset")
async def request_password_reset():
    """
    Endpoint to request a password reset.
    This endpoint will handle sending a password reset link to the user's email.
    """
    return {"message": "Password reset requested"}

@user_router.post("/verify-password-reset/{reset_token}", summary="Request password reset")
async def request_password_reset(reset_token:str):
    """
    Endpoint to request a password reset.
    This endpoint will handle sending a password reset link to the user's email.
    """
    return {"message": "Password reset requested"}

@user_router.put("/reset-password", summary="Reset user password")
async def reset_password():
    """
    Endpoint to reset user password.
    This endpoint will handle the logic for resetting the user's password.
    """
    return {"message": "Password reset endpoint"}

@user_router.get("/{user_id}", summary="Get user details")
async def get_user(user_id: str):
    """
    Endpoint to get details of a specific user by user ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        dict: User details.
    """
    return {"user_id": user_id, "message": "User details retrieved successfully"}

@user_router.put("/{user_id}", summary="Update user details")
async def update_user(user_id: str):
    """
    Endpoint to update user details.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        dict: Confirmation message of user details update.
    """
    return {"user_id": user_id, "message": "User details updated successfully"}

