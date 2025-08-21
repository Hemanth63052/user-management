from dotenv import load_dotenv

load_dotenv()

from typing import Any

from pydantic_settings import BaseSettings
from pydantic import model_validator


class _ModuleConfig(BaseSettings):
    """
    Configuration settings for the module.
    This class is used to load environment variables and provide access to them.
    """
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD_ASGI: bool = True
    CORS_ORIGINS: list[str] = ['*']
    DOMAIN_URL: str = "http://localhost:8000"
    APP_NAME: str = "Adapt IQ"

    @model_validator(mode="before")
    def validate(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the configuration settings.
        This method can be used to add custom validation logic if needed.

        Args:
            values (Any): The values to validate.
        Returns:
            Self: The validated configuration instance.
        """
        if "RELOAD_ASGI" in values:
            values['RELOAD_ASGI'] = values['RELOAD_ASGI'] in ('true', '1')
        if "CORS_ORIGINS" in values:
            if isinstance(values["CORS_ORIGINS"], str):
                values["CORS_ORIGINS"] = values["CORS_ORIGINS"].strip().split(",")
        if "DOMAIN_URL" not in values or not values["DOMAIN_URL"]:
            raise ValueError("DOMAIN_URL must be provided")
        if "DOMAIN_URL" in values:
            values["DOMAIN_URL"] = values["DOMAIN_URL"].strip().rstrip('/')
        return values


class _JWTConfig(BaseSettings):
    """
    Configuration settings for JWT.
    This class is used to load environment variables related to JWT.
    """
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # default to 1 hour

    @model_validator(mode="before")
    def validate(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the JWT configuration settings.
        This method can be used to add custom validation logic if needed.

        Args:
            values (Any): The values to validate.
        Returns:
            Self: The validated JWT configuration instance.
        """
        if "JWT_SECRET_KEY" not in values or not values["JWT_SECRET_KEY"]:
            raise ValueError("JWT_SECRET_KEY must be provided")
        return values

class _SQLConfig(BaseSettings):
    """
    Configuration settings for SQL.
    This class is used to load environment variables related to SQL database connection.
    """
    SQL_URL: str
    SQL_DATABASE: str = "user_management_db"

    @model_validator(mode="before")
    def validate(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the SQL configuration settings.
        This method can be used to add custom validation logic if needed.

        Args:
            values (Any): The values to validate.
        Returns:
            Self: The validated SQL configuration instance.
        """
        if "SQL_URL" not in values or not values["SQL_URL"]:
            raise ValueError("SQL_URL must be provided")
        values["SQL_URL"] = values["SQL_URL"].strip().rstrip('/')
        return values

class _EmailConfig(BaseSettings):
    """
    Configuration settings for email.
    This class is used to load environment variables related to email settings.
    """
    SMTP_SERVER: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    ALLOW_SSL: bool = True

    @model_validator(mode="before")
    def validate(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the email configuration settings.
        This method can be used to add custom validation logic if needed.

        Args:
            values (Any): The values to validate.
        Returns:
            Self: The validated email configuration instance.
        """
        if "SMTP_SERVER" not in values or not values["SMTP_SERVER"]:
            raise ValueError("SMTP_SERVER must be provided")
        if "ALLOW_SSL" in values and  isinstance(values['ALLOW_SSL'], str):
            values['ALLOW_SSL'] = values['ALLOW_SSL'].lower() in ('true', '1')
        return values


ModuleConfig = _ModuleConfig()
JWTConfig = _JWTConfig()
SQLConfig = _SQLConfig()
EmailConfig = _EmailConfig()

__all__ = ["ModuleConfig", "JWTConfig", "SQLConfig", "EmailConfig"]
