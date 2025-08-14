from scripts.config import JWTConfig
from datetime import datetime, timedelta
import jwt


class JWTUtil:

    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Create a JWT access token with the given data and expiration time.

        Args:
            data (dict): The data to include in the token.

        Returns:
            str: The generated JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=JWTConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWTConfig.JWT_SECRET_KEY, algorithm=JWTConfig.JWT_ALGORITHM)

    @staticmethod
    def generate_email_verification_token(email: str) -> str:
        """
        Generate a JWT token for email verification.

        Args:
            email (str): The email address to include in the token.

        Returns:
            str: The generated JWT token for email verification.
        """
        data = {"email": email}
        return JWTUtil.create_access_token(data)

    @staticmethod
    def request_reset_password_token(data:dict) -> str:
        """
        Generate a JWT token for password reset request.

        Args:
            data: dict: The data to include in the token, typically containing the user's email.

        Returns:
            str: The generated JWT token for password reset.
        """
        return JWTUtil.create_access_token(data)