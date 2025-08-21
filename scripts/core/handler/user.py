import asyncio
import datetime

from scripts.core.db.sql import SQLHandler
from scripts.core.services.email import verify_email, reset_password
from scripts.core.schemas.users import RegisterUser, LoginUser, PasswordReset, UpdateUserData
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
        :param response: fastapi response
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
        reset_token = JWTUtil.request_reset_password_token(
            {"user_id": user.id, "email": user.email}
        )
        # Here you would typically send the reset token to the user's email
        self.sql_handler.update_user_metadata({
            "reset_token": reset_token,
            "reset_token_expiry": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        }, filter_condition={"user_id": user.id
                             })
        asyncio.create_task(reset_password.ResetPassword(
            reset_token = reset_token,
            to_email=user.email,
        ))
        return {
            "status": "success",
            "message": "Password reset requested. Check your email for the reset link.",
        }

    async def verify_reset_password(self, reset_token: str):
        """
        Verify the request reset details
        :param reset_token: Reset token from email
        """
        user_metadata = await self.sql_handler.get_user_metadata(reset_token=reset_token)
        if not user_metadata:
            raise UserManagementException("Password Reset Expired. Please try again afresh")
        return {
            "status": "success",
            "message": "Reset Token verified successfully"
        }

    async def reset_password(self, reset_password_payload: PasswordReset):
        """
        Reset the password for the user
        :param reset_password_payload: Reset password payload with email and password
        """
        reset_password_payload.password = PasswordHashingUtil.hash_password(reset_password_payload.password)
        self.sql_handler.update_user({
            "password": reset_password_payload.password
        }, filter_condition={"email": reset_password_payload.email})
        return {
            "status":"success",
            "message": "Password Reset is done successfully, Please login with new password"
        }
    async def request_email_verify(self, email: str):
        """
        This function email the user to verify

        :param email: Email to verify
        """
        user = await self.sql_handler.check_user_exists_by_mail(email)
        if not user:
            raise UserManagementException("User with this email does not exist.")
        user = user[0]
        reset_token = JWTUtil.request_reset_password_token(
            {"user_id": str(user.id), "email": str(user.email)}
        )
        verify_handler = verify_email.VerifyEmailHandler()
        asyncio.create_task(verify_handler(
            to_email=user.email,
            verification_token=reset_token,
            user_name=f"{user.first_name} {user.last_name}"
        ))
        return {
            "status": "success",
            "message": "An email has been sent to verify your. Please follow the instructions mentioned"
        }

    async def verify_email(self, verification_token: str):
        """
        Verify the email using the verification token.

        :param verification_token: Token to verify the email.
        :return: Confirmation message.
        """
        user_metadata = await self.sql_handler.get_user_metadata_by_verification_token(verification_token=verification_token)
        if not user_metadata:
            raise UserManagementException("Email Verification Expired. Please try again afresh")
        self.sql_handler.update_user_metadata(
            {"email_verified": True, "email_verification_token": None},
            filter_condition={"user_id": user_metadata.user_id}
        )
        return {
            "status": "success",
            "message": "Email verified successfully."
        }

    async def get_user(self, email:str):
        user = await self.sql_handler.check_user_exists_by_mail(email=email)
        if not user:
            raise UserManagementException("User with this email does not exist.")
        user = user[0]
        return user

    async def get_user_by_id(self, user_id: str):
        user = await self.sql_handler.get_user_by_id(user_id=user_id)
        return {
            "status": "success",
            "message":"User data fetched successfully",
            "data":user
        }

    async def update_user_data_by_id(self, user_data: UpdateUserData):
        user_info = await self.get_user_by_id(user_id=user_data.user_id)
        if not user_info.get("data"):
            raise UserManagementException("User with this email does not exist.")
        self.sql_handler.update_user(user_data=user_data.model_dump(exclude={"user_id", "user_metadata"}),
                                     filter_condition={"id":user_data.user_id})
        self.sql_handler.update_user_metadata(
            user_metadata=user_data.user_metadata.model_dump(),
            filter_condition={"user_id":user_data.user_id}
        )
        return {
            "status":"success",
            "message":"User info updated successfully"
        }



