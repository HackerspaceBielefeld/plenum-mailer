import smtplib
import ssl

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from coolname import generate_slug


def get_second_thursday():
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

def sent_mail(second_thursday: str):
    sender_email = "<SENDER_MAIL_ADDRESS>"
    password = "<PASSWORD>"
    smtp_server = "<SMTP_SERVER>"
    receiver_email = "<MAILINGLIST>"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Einladung zum Plenum am {second_thursday} - 20:00 Uhr"

    # Add body to email
    body = (
        "Hallo zusammen,\n"
        f"am Donnerstag {second_thursday} findet wie gewohnt das Plenum statt.\n"
        "Teilnehmen könnt ihr natürlich in Präsenz oder online über unser Jitsi.\n\n"

        f"Online Teilnahme: https://conference.space.bi/{generate_slug(2).replace('-', '')}\n"
        "Themen: https://wiki.hackerspace-bielefeld.de/index.php?title=Plenum\n\n"
        
        "Viele Grüße\n"
    )

    message.attach(MIMEText(body, "plain"))
    content = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, content)

    return True

def main():
    today = datetime.now().strftime("%d.%m.%Y")
    second_thursday = get_second_thursday()
    tuesday_before = second_thursday - timedelta(days=2)

    # Ensure it's tuesday before the second thursday
    if today != tuesday_before.strftime("%d.%m.%Y"):
        print("No mail was sent because it's not tuesday before the second thursday")
        return
    
    sent_mail(second_thursday.strftime("%d.%m.%Y"))
    return


if __name__ == "__main__":
    main()
