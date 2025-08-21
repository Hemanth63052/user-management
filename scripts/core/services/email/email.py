from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL, SMTP
from scripts.config import EmailConfig


class EmailUtil:

    @staticmethod
    def connect():
        """
        Connect to the email server.
        This method should be implemented to establish a connection to the email server.
        """
        if EmailConfig.ALLOW_SSL:
            smtp_client = SMTP_SSL(
                host=EmailConfig.SMTP_SERVER,
                port=EmailConfig.SMTP_PORT,
            )
        else:
            smtp_client = SMTP(
                host=EmailConfig.SMTP_SERVER,
                port=EmailConfig.SMTP_PORT,
            )
            smtp_client.starttls()
        smtp_client.login(EmailConfig.SMTP_USERNAME, EmailConfig.SMTP_PASSWORD)
        return smtp_client

    def send_email(self, message: MIMEMultipart, ssl: bool = False):
        """
        Send an email message.

        Args:
            message (MIMEMultipart): The email message to send.
            ssl (bool): Whether to use SSL for the connection. Defaults to False.
        """
        if not message["From"]:
            message["From"] = EmailConfig.EMAIL_FROM
        smtp_client = self.connect()
        smtp_client.send_message(message)
        smtp_client.quit()
