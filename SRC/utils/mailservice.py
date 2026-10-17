import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
def send_email(to_email:str,subject:str,body:str):
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=os.environ["Email_Address"]
    msg["To"]=to_email
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(
            os.environ["Email_Address"],
            os.environ["Email_App_Password"]
        )
        server.send_message(msg)
        