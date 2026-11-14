import smtplib
import ssl
from email.message import EmailMessage

sender = input("Your Gmail address: ").strip()
receiver = input("who do you want to send to?: ").strip()
app_password = input("Gmail app password: ").strip()

# Email 2: with attachment
second_email = EmailMessage()
second_email["From"] = sender
second_email["To"] = receiver
second_email["Subject"] = "second email from Hagay with attachment"
second_email.set_content("email with attached file")


file_path = "cowboy.png"
with open(file_path, "rb") as file:
    second_email.add_attachment(
        file.read(),
        maintype="image",
        subtype="png",
        filename="cowboy.png"
    )


context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, app_password)
    server.send_message(second_email)
