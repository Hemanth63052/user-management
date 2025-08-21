from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from scripts.config import ModuleConfig, JWTConfig, EmailConfig
from scripts.core.services.email import EmailHandler
from scripts.exceptions import UserManagementException


class VerifyEmailHandler(EmailHandler):
    """
    This class handles the verification of user emails.
    It extends the EmailHandler to provide specific functionality
    for verifying user emails using a verification token.

    """
    def __init__(self):
        super().__init__()

    async def create_mime_message(self, *args, **kwargs) -> MIMEMultipart:
        """
        Create a MIME message for email verification.

        :return: MIMEMultipart object containing the email message.
        """
        to_email = kwargs.get("to_email")
        if not to_email:
            print("To Email not found for resetting password")
            raise UserManagementException("Failed to reset password. Please try again Later")
        html_path = "scripts/core/services/email/verify_email/template.html"
        html_content = await self.fetch_html_content(html_path=html_path)
        replace_payload = {
                        "user_name": kwargs.get("user_name", "There"),
                        "app_name": ModuleConfig.APP_NAME,
                        "user_email": to_email,
                        "expires_in": f"{kwargs.get('expires_in', JWTConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)} Minutes",
                        "verify_url": f"{ModuleConfig.DOMAIN_URL}/verify-email/{kwargs.get('verification_token')}",
                        "support_email": f"{EmailConfig.SMTP_USERNAME}",
                        "year": datetime.now(tz=timezone.utc).year
                    }
        html_content = await self.replace_html_content(html_content=html_content, replace_payload=replace_payload)
        message = MIMEMultipart("alternative")
        message["To"] = to_email
        message["Subject"] = f"Re: Verify your email for {ModuleConfig.APP_NAME}"
        message.attach(MIMEText(html_content, "html"))
        return message
