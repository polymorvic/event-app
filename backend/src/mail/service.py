from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from src.mail.connection import conf


async def send_verification_mail(receiver_email: str, verification_token: str) -> None:
    verification_url = f"http://localhost:8000/auth/verify-email/{verification_token}"
    html = f"""
    <html>
        <body>
        <h1>Welcome</h1>
        <p>Thank you for using event-app <a href={verification_url}>Verify Email</a></p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to Event App",
        recipients=[receiver_email],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
