"""
This will be the entry point for the application
It will read, write, and send the email to the recipients
"""
from email_writer import write_email
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import os

def send_email(group_id: str):
    load_dotenv()
    EMAIL_USER = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    recipients, subject, body = write_email(group_id)

    for recipient in recipients:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = recipient

        msg.set_content("An error has occurred.  We could not deliver your blog.")
        msg.add_alternative(body, subtype="html")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)

# TODO: Add in clean up where MongoDB values don't persist after a month