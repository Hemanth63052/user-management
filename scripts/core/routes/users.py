from fastapi import APIRouter, Depends, Response

from scripts.core.schemas.users import RegisterUser, LoginUser, RequestEmailVerify, PasswordResetRequest, PasswordReset
from scripts.core.handler.user import UserHandler
from scripts.db.pg.sessions import get_db

user_router = APIRouter(prefix="/users", tags=["Users"], redirect_slashes=True)

@user_router.post("/register", summary="Register a new user")
async def register_user(register_data: RegisterUser, session = Depends(get_db)):
    """
    Endpoint to register a new user.
    This endpoint will handle user registration logic.
    """
    return await UserHandler(session=session).register_user(register_data=register_data)

@user_router.post("/login", summary="User login")
async def login_user(login_data:LoginUser,  response: Response, session = Depends(get_db)):
    """
    Endpoint for user login.
    This endpoint will handle user authentication and return a token.
    """
    return await UserHandler(session=session).login_user(response=response, login_data=login_data)

@user_router.post("/request-email-verify/{email}", summary="Request Email verify")
async def request_email_verify(email_payload:RequestEmailVerify, session = Depends(get_db)):
    """
    Endpoint for Sending an email to verify the user
    :param email_payload:
    :param session:
    :return:
    """
    return await UserHandler(session=session).request_email_verify(email=email_payload.email)

@user_router.put("/verify-email/{verification_token}", summary="Verify user email")
async def verify_email(verification_token: str, session = Depends(get_db)):
    """
    Endpoint to verify user email using a verification token.

    Args:
        verification_token (str): The token used for email verification.
        session
    Returns:
        dict: Confirmation message of email verification.
    """
    return await UserHandler(session=session).verify_email(verification_token=verification_token)

@user_router.post("/request-password-reset", summary="Request password reset")
async def request_password_reset(reset_password_payload:PasswordResetRequest, session = Depends(get_db)):
    """
    Endpoint to request a password reset.
    :param reset_password_payload: Payload which accepts the email to reset password
    :param session:
    This endpoint will handle sending a password reset link to the user's email.
    """
    return await UserHandler(session=session).request_reset_password(reset_data=reset_password_payload.model_dump())

@user_router.post("/verify-password-reset/{reset_token}", summary="Request password reset")
async def request_password_reset(reset_token:str, session = Depends(get_db)):
    """
    Endpoint to request a password reset.
    This endpoint will handle sending a password reset link to the user's email.
    """
    return await UserHandler(session=session).verify_reset_password(reset_token=reset_token)

@user_router.put("/reset-password", summary="Reset user password")
async def reset_password(reset_password_payload:PasswordReset,   session = Depends(get_db)):
    """
    Endpoint to reset user password.
    This endpoint will handle the logic for resetting the user's password.
    """
    return await UserHandler(session=session).reset_password(reset_password_payload=reset_password_payload)

