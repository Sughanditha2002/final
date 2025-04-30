from builtins import bool, int, str
from pathlib import Path
from pydantic import Field, AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # General
    max_login_attempts: int = Field(default=3, description="Max login attempts before lockout")

    # Server configuration
    server_base_url: AnyUrl = Field(default='http://localhost', description="Base URL of the server")
    server_download_folder: str = Field(default='downloads', description="Folder for storing downloaded files")

    # Security and authentication
    secret_key: str = Field(default="secret-key", description="Secret key for encryption")
    algorithm: str = Field(default="HS256", description="Algorithm used for encryption")
    access_token_expire_minutes: int = Field(default=15, description="Access token expiry in minutes")
    refresh_token_expire_minutes: int = Field(default=1440, description="Refresh token expiry in minutes")
    admin_user: str = Field(default='admin', description="Default admin username")
    admin_password: str = Field(default='secret', description="Default admin password")
    debug: bool = Field(default=False, description="Enable debug mode")
    jwt_secret_key: str = "a_very_secret_key"
    jwt_algorithm: str = "HS256"

    # Database configuration
    database_url: str = Field(default='postgresql+asyncpg://user:password@postgres/myappdb')
    postgres_user: str = Field(default='user')
    postgres_password: str = Field(default='password')
    postgres_server: str = Field(default='localhost')
    postgres_port: str = Field(default='5432')
    postgres_db: str = Field(default='myappdb')

    # Discord
    discord_bot_token: str = Field(default='NONE')
    discord_channel_id: int = Field(default=1234567890)

    # OpenAI Key
    openai_api_key: str = Field(default='NONE')
    send_real_mail: bool = Field(default=False)

    
    mail_username: str = Field(default='your@mail.com', description="MAIL_USERNAME")
    mail_password: str = Field(default='yourpassword', description="MAIL_PASSWORD")
    mail_from: str = Field(default='your@mail.com', description="MAIL_FROM")
    mail_port: int = Field(default=587, description="MAIL_PORT")
    mail_server: str = Field(default='smtp.mailtrap.io', description="MAIL_SERVER")
    mail_starttls: bool = Field(default=True, description="MAIL_STARTTLS")
    mail_ssl_tls: bool = Field(default=False, description="MAIL_SSL_TLS")
    use_credentials: bool = Field(default=True, description="USE_CREDENTIALS")
    validate_certs: bool = Field(default=True, description="VALIDATE_CERTS")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
