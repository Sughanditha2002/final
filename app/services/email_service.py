from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.models.user_model import User
from settings.config import settings
from app.utils.template_manager import TemplateManager
from app.utils.smtp_connection import SMTPClient

# Define Mailtrap configuration (for Mailtrap SMTP settings)
config = ConnectionConfig(
    MAIL_USERNAME="sd2388",  # Your Mailtrap username
    MAIL_PASSWORD="Njit@20242024",  # Your Mailtrap password
    MAIL_FROM="sd2388@njit.edu",  # The email from which you want to send emails
    MAIL_PORT=587,  # Mailtrap SMTP port
    MAIL_SERVER="smtp.mailtrap.io",  # Mailtrap SMTP server
    MAIL_TLS=True,  # Use TLS for security
    MAIL_SSL=False,  # Disable SSL (Mailtrap uses TLS)
)

# Create an instance of FastMail (Mailtrap client)
mail = FastMail(config)

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        """
        Method to send an email to the user based on the email type.
        """
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        # Render email content using the template
        html_content = self.template_manager.render_template(email_type, **user_data)

        # Sending email via SMTPClient
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        """
        Send a verification email to the user with the verification link.
        """
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"

        # Prepare user data for the email template
        user_data = {
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }

        # Send the verification email
        await self.send_user_email(user_data, 'email_verification')
        
    async def send_email_via_fastapi_mail(self, user: User):
        """
        Sends an email through FastAPI Mail (Mailtrap)
        """
        # Compose the email message
        message = MessageSchema(
            subject="Verify Your Account",
            recipients=[user.email],
            body=f"Hello {user.first_name},\n\nPlease verify your email using the following link: {settings.server_base_url}verify-email/{user.id}/{user.verification_token}",
            subtype="html"
        )
        
        # Send the email using FastMail
        await mail.send_message(message)