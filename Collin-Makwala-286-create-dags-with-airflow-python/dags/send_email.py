import os
import smtplib
from email.mime.text import MIMEText

from dags.github_pr_utils import get_top_5_pull_requests


def get_smtp_settings():
    smtp_server = os.getenv("SMTP_SERVER")
    port = os.getenv("SMTP_PORT")
    login = os.getenv("SMTP_LOGIN")
    password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    smtp_settings = [smtp_server, port, login, password, sender_email, receiver_email]
    if not all(smtp_settings):
        raise ValueError(
            "smtp settings (server, port, login, password, sender_email, receiver_email) must be set."
        )

    return smtp_server, port, login, password, sender_email, receiver_email


def create_message():
    sender_email, receiver_email = get_smtp_settings()[4:]
    top_5_prs = get_top_5_pull_requests()

    email_body = f"Here are the top 5 PRs that need attention in order of priority:\n{top_5_prs}"

    message = MIMEText(email_body)
    message["Subject"] = "Top 5 Pull Request Reviews for the day"
    message["From"] = sender_email
    message["To"] = receiver_email

    return message


def send_email():
    smtp_server, port, login, password, sender_email, receiver_email = get_smtp_settings()


    message = create_message()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__":
    send_email()
