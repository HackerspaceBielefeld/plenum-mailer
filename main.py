import smtplib
import ssl
import os

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from coolname import generate_slug
from dotenv import load_dotenv

from Matrix import Matrix

# Load environment variables from .env file
load_dotenv()

# mail
SENDER_MAIL = os.getenv("SENDER_MAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
RECEIVER_MAIL = os.getenv("RECEIVER_MAIL")
# matrix
MATRIX_SERVER_URL = os.getenv("MATRIX_SERVER_URL")
MATRIX_USERNAME = os.getenv("MATRIX_USERNAME")
MATRIX_PASSWORD = os.getenv("MATRIX_PASSWORD")
MATRIX_ROOM_ID = os.getenv("MATRIX_ROOM_ID")

def get_second_thursday() -> None:
    # Get the current date
    now = datetime.now()
    year = now.year
    month = now.month

    # Find the first day of the current month
    first_day = datetime(year, month, 1)
    # Calculate the weekday of the first day of the month (0=Monday, 1=Tuesday, ..., 6=Sunday)
    first_weekday = first_day.weekday()
    # Calculate the days to the first Thursday (3 = Thursday)
    days_to_first_thursday = (3 - first_weekday + 7) % 7
    # Calculate the date of the first Thursday
    first_thursday = first_day + timedelta(days=days_to_first_thursday)
    # Calculate the date of the second Thursday
    second_thursday = first_thursday + timedelta(days=7)

    return second_thursday

def check_correct_date(second_thursday: datetime) -> bool:
    today = datetime.now().strftime("%d.%m.%Y")
    tuesday_before = second_thursday - timedelta(days=2)

    # Ensure it's tuesday before the second thursday
    if today != tuesday_before.strftime("%d.%m.%Y"):
        return False
    return True


def send_matrix_message(server_url: str, username: str, password: str, room_id: str, message: str, subject: str) -> None:
    matrix=Matrix(
        username=username,              # Matrix username (without homeserver)
        password=password,              # Matrix password
        homeserver=server_url,          # Matrix homeserver
        room_id=room_id,                # Room ID
    )

    message_raw = subject + "\n" + message
    message_html = "<h1>" + subject + "</h1>" + message.replace("\n", "<br>")

    matrix.send(message_raw, message_html)

def sent_mail(body: str, subject: str) -> None:
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SENDER_MAIL
    message["To"] = RECEIVER_MAIL
    message["Subject"] = subject
    message["Date"] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    content = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, 465, context=context) as server:
        server.login(SENDER_MAIL, PASSWORD)
        server.sendmail(SENDER_MAIL, RECEIVER_MAIL, content)

def main() -> None:
    second_thursday = get_second_thursday()
    second_thursday_format = second_thursday.strftime("%d.%m.%Y")
    if not check_correct_date(second_thursday):
        print("wrong date, nothing sent")
        return
    
    subject = f"Einladung zum Plenum am {second_thursday_format} - 20:00 Uhr"
    body = (
        "Hallo zusammen,\n"
        f"am Donnerstag {second_thursday_format} findet wie gewohnt das Plenum statt.\n"
        "Teilnehmen könnt ihr natürlich in Präsenz oder online über unser Jitsi.\n\n"

        f"Online Teilnahme: https://conference.space.bi/{generate_slug(2).replace('-', '')}\n"
        "Themen: https://wiki.hackerspace-bielefeld.de/index.php?title=Plenum\n\n"
        
        "Viele Grüße\n"
    )

    # Sent Mail
    sent_mail(body, subject)
    # Sent Matrix
    send_matrix_message(MATRIX_SERVER_URL, MATRIX_USERNAME, MATRIX_PASSWORD, MATRIX_ROOM_ID, body, subject)
    return

if __name__ == "__main__":
    main()
