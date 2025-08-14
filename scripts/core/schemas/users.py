from pydantic import BaseModel

class RegisterUser(BaseModel):
    """
    Schema for registering a new user.
    This schema is used to validate the data when a new user registers.
    """
    email: str
    first_name: str
    last_name: str
    password: str
    role: str | None = None
    phone_number: str | None = None
    address: str | None = None


class LoginUser(BaseModel):
    """
    Schema for user login.
    This schema is used to validate the data when a user logs in.
    """
    email: str
    password: str


class UpdateUser(BaseModel):
    """
    Schema for updating user details.
    This schema is used to validate the data when a user updates their profile.
    """
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    address: str | None = None
    role: str | None = None


class PasswordResetRequest(BaseModel):
    """
    Schema for requesting a password reset.
    This schema is used to validate the data when a user requests a password reset.
    """
    email: str

class PasswordReset(BaseModel):
    """
    Schema for resetting a user's password.
    This schema is used to validate the data when a user resets their password.
    """
    reset_token: str
    new_password: str

