import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

def send_email_alert(subject: str, message: str, to_email: str):

    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not app_password:
        print("Email credentials not configured")
        return

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content(message)

    try:

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(sender_email, app_password)

            smtp.send_message(msg)

        print("Email alert sent")

    except Exception as e:

        print(f"Email alert failed: {e}")
