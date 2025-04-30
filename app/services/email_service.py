from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.models.user_model import User
from settings.config import settings
from app.utils.template_manager import TemplateManager
from app.utils.smtp_connection import SMTPClient

# ✅ FastAPI-Mail configuration using values from settings
config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs
)

# ✅ FastAPI-Mail instance
mail = FastMail(config)

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.mail_server,
            port=settings.mail_port,
            username=settings.mail_username,
            password=settings.mail_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        """
        Send an email using the template and SMTPClient based on email_type.
        """
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        """
        Send a verification email with a verification link using SMTPClient.
        """
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        user_data = {
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }
        await self.send_user_email(user_data, 'email_verification')
        
    async def send_email_via_fastapi_mail(self, user: User):
        """
        Send a verification email using FastAPI-Mail.
        """
        message = MessageSchema(
            subject="Verify Your Account",
            recipients=[user.email],
            body=(
                f"Hello {user.first_name},<br><br>"
                f"Please verify your email using the following link: "
                f"<a href='{settings.server_base_url}verify-email/{user.id}/{user.verification_token}'>Verify Email</a>"
            ),
            subtype="html"
        )
        await mail.send_message(message)
