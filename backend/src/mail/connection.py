from fastapi_mail import ConnectionConfig
from src.secrets import email_password, email_username, email_from


conf = ConnectionConfig(
    MAIL_USERNAME=email_username(),
    MAIL_PASSWORD=email_password(),
    MAIL_FROM=email_from(),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
