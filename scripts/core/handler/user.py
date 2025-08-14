import asyncio
import datetime

from scripts.core.handler.db_handler.sql import SQLHandler
from scripts.core.schemas.users import RegisterUser, LoginUser
from scripts.exceptions import UserManagementException
from scripts.utils.jwt import JWTUtil
from scripts.utils.password import PasswordHashingUtil
from fastapi import Response


class UserHandler:
    """
    UserHandler class to manage user-related operations.
    This class will handle user login, registration, email verification,
    password reset, and user details management.
    """

    def __init__(self, session):
        self.sql_handler = SQLHandler(session=session)

    async def register_user(self, register_data: RegisterUser):
        """
        Register a new user with the provided registration data.

        :param register_data: Data required for user registration.
        :return: Confirmation message or user details.
        """
        if await self.sql_handler.check_user_exists_by_mail(register_data.email):
            raise UserManagementException("User with this email already exists.")
        register_data.password = PasswordHashingUtil.hash_password(register_data.password)
        user = self.sql_handler.insert_new_user(register_data.model_dump(exclude={"phone_number", "address"}))
        self.sql_handler.insert_user_metadata({
            "phone_number": register_data.phone_number,
            "address": register_data.address,
            "user_id": user.id,
        })
        return {
            "status": "success",
            "message": "User registered successfully.",
        }

    async def login_user(self, response: Response, login_data: LoginUser):
        """
        Log in a user with the provided login data.

        :param login_data: Data required for user login.
        :return: Confirmation message or user details.
        """
        user = await self.sql_handler.check_user_exists_by_mail(login_data.email)
        if not user:
            raise UserManagementException("User with this email does not exist.")

        if not PasswordHashingUtil.verify_password(login_data.password, user.password):
            raise UserManagementException("Invalid password.")
        # Here you would typically generate a token and set it in the response headers
        access_token = JWTUtil.create_access_token({
            "user_id": user.id,
            "email": user.email,
        })
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # Set to True if using HTTPS
        )
        return {
            "status": "success",
            "message": "User logged in successfully.",
            "user_id": user.id,
        }

    async def request_reset_password(self, reset_data: dict):
        """
        Reset a user's password with the provided reset data.

        :param reset_data: Data required for password reset.
        :return: Confirmation message or user details.
        """
        user = await self.sql_handler.check_user_exists_by_mail(reset_data['email'])
        if not user:
            raise UserManagementException("User with this email does not exist.")
        user = user[0]
        reset_token = JWTUtil.request_reset_password_token(
            {"user_id": user.id, "email": user.email}
        )
        # Here you would typically send the reset token to the user's email
        self.sql_handler.update_user_metadata({
            "reset_token": reset_token,
            "reset_token_expiry": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        }, filter_condition={"user_id": user.id
                             })
        asyncio.create_task(

        )
        return {
            "status": "success",
            "message": "Password reset requested. Check your email for the reset link.",
        }
