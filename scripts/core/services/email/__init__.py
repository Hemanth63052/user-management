from email.mime.multipart import MIMEMultipart
from abc import abstractmethod

from jinja2 import Environment, BaseLoader

from scripts.core.services.email.email import EmailUtil

class EmailHandler:
    """
    Base class for handling email operations.
    This class can be extended to implement specific email handling logic.
    """

    def __init__(self):
        self.email_util = EmailUtil()

    async def send_email(self, mime_message: MIMEMultipart):
        """
        Send an email using the provided MIME message.

        :param mime_message: The MIME message to be sent.
        """
        self.email_util.send_email(mime_message)

    @abstractmethod
    async def create_mime_message(self, *args, **kwargs)-> MIMEMultipart:
        """
        Create a MIME message for sending an email.
        :return: A MIMEMultipart object representing the email message.
        """
        raise NotImplemented("create_mime_message method must be implemented in subclasses")

    @staticmethod
    async def fetch_html_content(html_path:str="template.html"):
        """
        This func is used to load the HTML Content
        :param html_path:
        :return:
        """
        with open(html_path, "r") as html_file:
            html_content = html_file.read()
        return html_content

    @staticmethod
    async def replace_html_content(html_content, replace_payload):
        env = Environment(loader=BaseLoader())
        template = env.from_string(html_content)
        rendered_html = template.render(replace_payload)
        return rendered_html

    async def __call__(self, *args, **kwargs):
        """
        Call method to handle email operations.
        :param args:
        :param kwargs:
        :return:
        """
        mime_message = await self.create_mime_message(*args, **kwargs)
        await self.send_email(mime_message)
        return True
