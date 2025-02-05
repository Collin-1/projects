import os
import re
import json
import logging
import sys
import smtplib
from email.mime.text import MIMEText

import requests


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler() # Create a stream handler for logging
logger.addHandler(stream_handler)


def get_quote():
    """Fetch a quote of the day from the FavQs API"""

    try:
        response = requests.get("https://favqs.com/api/qotd")
        response.raise_for_status()
        quote = {
            key: value
            for key, value in response.json()["quote"].items()
            if key in ["author", "body"]
        }
        return quote
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e

def get_smtp_settings():
    """Retrieve SMTP settings from environment variables"""

    smtp_server = os.getenv("SMTP_SERVER")
    port = os.getenv("SMTP_PORT")
    login = os.getenv("SMTP_LOGIN")
    password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")

    smtp_settings = [smtp_server, port, login, password, sender_email]

    #Raises: ValueError: If any of the SMTP settings are not set
    if not all(smtp_settings): 
        logger.error("smtp settings (server, port, login, password, sender_email) must be set.")
        raise ValueError(
            "smtp settings (server, port, login, password, sender_email) must be set."
        )

    return smtp_server, port, login, password, sender_email


def validate_emails(receiver_emails):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    for receiver_email in receiver_emails:
        email = receiver_email["email"]
        if not re.fullmatch(pattern, email):
            logger.error(f"The reciever email, {email}, is not valid")
            raise ValueError(f"The reciever email, {email}, is not valid")


def validate_json_file(file_path):
    try:
        with open(os.path.expanduser(file_path), "r") as file:
            receiver_emails = json.load(file)
    except FileNotFoundError as no_file:
        logger.error(no_file)
        raise no_file
    except json.decoder.JSONDecodeError:
        logger.error("The file contains an invalid JSON")
        raise ValueError("The file contains an invalid JSON")
    
    if not isinstance(receiver_emails, list):
        logger.error("The Json file must contain a list")
        raise ValueError("The Json file must contain a list")

    for dictionanry in receiver_emails:
        if not isinstance(dictionanry, dict):
            logger.error("Each item in the list should be a dictionary")
            raise ValueError("Each item in the list should be a dictionary")
        if not {"email", "name"}.issubset(dictionanry.keys()):
            logger.error("Each dictionary should contain 'email' and 'name' keys")
            raise ValueError("Each dictionary should contain 'email' and 'name' keys")

    return receiver_emails


def validate_cmd_args(receiver_emails):
    """Validate the command-line arguments for receiver emails."""

    if len(receiver_emails) == 2:
        if receiver_emails[1] != "--same":
            logger.error("Behaviour must be '--same'")
            raise ValueError("Behaviour must be '--same'")

    if len(receiver_emails) > 2:
        logger.error("The argument must be an email_address/path_to_json and behaviour(--same)")
        raise ValueError(
            "The argument must be an email_address/path_to_json and behaviour(--same)"
        )


def get_receiver_email():
    """Retrieve and validate receiver email addresses from command-line arguments or a JSON file"""

    receiver_emails = sys.argv[1:] if len(sys.argv) > 1 else None
    if not receiver_emails:
        logger.error("Please provide a reciever email")
        raise ValueError("Please provide a reciever email")
    
    validate_cmd_args(receiver_emails)
    same_quote = receiver_emails[1:]

    if "~" in receiver_emails[0]:
        receiver_emails = validate_json_file(receiver_emails[0])
    else:
        receiver_emails = [{"email": receiver_emails[0], "name": None}]

    validate_emails(receiver_emails)

    return receiver_emails, same_quote


def create_message(quote, reciever_email):
    """ Create an email message with the given quote and receiver email information."""

    salutation = f'Dear {reciever_email["name"]},\n\n' if reciever_email["name"] else ""

    email_body = f'{salutation}"{quote["body"]}" - {quote["author"]}'

    message = MIMEText(email_body)
    message["Subject"] = "Inpirational quote"
    message["From"] = get_smtp_settings()[4]
    message["To"] = reciever_email["email"]

    return message


def send_email():
    """Send an email with an inspirational quote to the receiver email addresses."""

    smtp_server, port, login, password, sender_email = get_smtp_settings()
    receiver_emails, condition = get_receiver_email()

    qoutes_list = (
        [get_quote()] * len(receiver_emails)
        if condition
        else [get_quote() for _ in receiver_emails]
    )

    messages = [
        create_message(quote, receiver_email)
        for quote, receiver_email in zip(qoutes_list, receiver_emails)
    ]

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        for message, receiver_email in zip(messages, receiver_emails):
            server.sendmail(sender_email, receiver_email["email"], message.as_string())
    logger.info(f"email sent to {[receiver_email["email"] for receiver_email in  receiver_emails]}")


if __name__ == "__main__":
    # Set up a file handler for logging errors
    file_handler = logging.FileHandler("errors.log")
    file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)

    # Send the email
    send_email()
