import smtplib
import ssl
from email.message import EmailMessage

sender = input("Your Gmail address: ").strip()
receiver = input("who do you want to send to?: ").strip()
app_password = input("Gmail app password: ").strip()

first_email = EmailMessage()
first_email["From"] = sender
first_email["To"] = receiver
first_email["Subject"] = "email with smtp from Hagay"
first_email.set_content(
    "why do programmers like dark mode?"
    "\nbecause light attracts bugs"
)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, app_password)
    server.send_message(first_email)

