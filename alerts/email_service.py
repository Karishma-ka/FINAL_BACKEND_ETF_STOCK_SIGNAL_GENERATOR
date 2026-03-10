import smtplib
from email.message import EmailMessage


def send_email_alert(subject: str, message: str, to_email: str):

    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content(message)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

    except Exception as e:
        print(f"Email alert failed: {e}")