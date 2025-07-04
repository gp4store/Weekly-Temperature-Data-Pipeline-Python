import smtplib
import os
from dotenv import load_dotenv
from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()
day_stamp = datetime.today().strftime('%Y%m%d')
smtp_server = 'smtp.gmail.com'
port_server = 587

# Load enviroment variables from .env file
email = os.getenv('AUTOMATION_EMAIL')
password = os.getenv('AUTOMATION_PASS')
recipient = os.getenv('EMAIL_SENDER')

# Email content
subject = f'Daily temperature dashboard {day_stamp}'
emailbody = f'Todays {day_stamp} temperature readings are attached to this email'

# Headers creation
emailmessage = MIMEMultipart()
emailmessage["From"] = email
emailmessage["To"] = recipient
emailmessage["Subject"] = subject

# Attaching the message to the actual email
emailmessage.attach(MIMEText(emailbody, "plain"))

# File path where our dashboard is saved from create_dash.py
filename_path = f"/your/path/Weekly-Temperature-Data-Pipeline-Python/Dashboards/Daily_temperature_plot_{day_stamp}.png"

# Open the file in binary mode
with open(filename_path, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header("Content-Disposition", f"attachment; filename= {filename_path}")

# Add header as key/value pair to attachment part
# Use just the filename, not the full path
filename_only = os.path.basename(filename_path)
part.add_header("Content-Disposition", f"attachment; filename={filename_only}")

# Add attachment to message
emailmessage.attach(part)

try:
    with smtplib.SMTP(smtp_server, port_server) as server:
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient, emailmessage.as_string())
        print("Email was sent with no issues to recipient")
       
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication failed: {e}")
    print("Things to check: Email configuration, App password configured")
except FileNotFoundError:
    print(f"File not found: {filename_path}")
except Exception as e:
    print(f"Error sending email: {e}")
    




