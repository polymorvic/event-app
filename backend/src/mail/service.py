from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from src.mail.connection import conf


async def send_mail(receiver_email: str) -> None:
    html = f"""
    <html>
        <body>
        <h1>Welcome</h1>
        <p>Thank you for using event-app</p>
        </body>
    </html>
    """
    
    message = MessageSchema(
        subject="Welcome to Event App",
        recipients=[receiver_email],
        body=html,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)
    
    