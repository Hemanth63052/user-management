from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from scripts.config import ModuleConfig
from scripts.core.services.email import EmailHandler
from scripts.exceptions import UserManagementException


class ResetPassword(EmailHandler):
    """
    ResetPassword class to handle password reset email operations.
    This class will manage the sending of password reset emails and
    the verification of reset tokens.
    """

    def __init__(self):
        super().__init__()

    async def create_mime_message(self, *args, **kwargs) -> MIMEMultipart:
        """
        Create a MIME message for the password reset email.

        :return: MIMEMultipart object containing the email message.
        """
        html_path = "/scripts/core/services/email/reset_password/template.html"
        html_content = await self.fetch_html_content(html_path=html_path)
        reset_token = kwargs.get("reset_token")
        reset_url = ModuleConfig.DOMAIN_URL +f"/verify-password-reset/{reset_token}"
        html_content = html_content.replace("{{reset_url}}", reset_url)
        to_email = kwargs.get("to_email")
        if not to_email:
            print("To Email not found for resetting password")
            raise UserManagementException("Failed to reset password. Please try again Later")
        message = MIMEMultipart("alternative")
        message["To"] = to_email
        message["Subject"] = f"Re: Password Reset Request for {ModuleConfig.APP_NAME}"
        message.attach(MIMEText(html_content, "html"))
        return message






