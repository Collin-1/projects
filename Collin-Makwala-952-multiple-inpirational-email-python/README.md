# Inspirational Quote Email Sender

A Python command-line application that sends inspirational quotes via email. The application can send quotes to individual email addresses or to multiple recipients from a JSON file.

## Features

- Send random inspirational quotes via email
- Fetch quotes from FavQs API
- Support for single recipient or multiple recipients via JSON file
- Personalized emails with recipient names
- Option to send same or different quotes to multiple recipients

## Prerequisites

- Python 3.x
- SMTP email service account (Brevo recommended)
- Environment variables configured for SMTP settings

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/Collin-1/projects.git
    cd projects/Collin-Makwala-952-multiple-inpirational-email-python/
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    pip install -e .
    ```

4. Configure SMTP settings:

Create a smtp_secrets.sh file with your SMTP credentials:

    export SMTP_SERVER=your_smtp_server
    export SMTP_PORT=your_smtp_port
    export SMTP_LOGIN=your_login
    export SMTP_PASSWORD=your_password

5. Source the SMTP settings:

`source smtp_secrets.sh`

### Usage
Single Recipient
Send a quote to a single email address:

`python inspirational_emails/send_inspiration.py someone@email.com`

Multiple Recipients

Send quotes to multiple recipients using a JSON file:

`python send_inspiration.py ~/email_recipients.json`

Recipients JSON Format
```[
{
    "email": "someone@email.com",
    "name": "John Doe"
},
{
    "email": "another@email.com",
    "name": "Jane Smith"
}
]
```
Same Quote Option

To send the same quote to all recipients in a JSON file:

`python send_inspiration.py ~/email_recipients.json --same`

Project Structure
```
├── inspirational_emails/     # Main package directory
│   ├── __init__.py
│   ├── quote_sender.py      # Core functionality
│   ├── email_handler.py     # Email handling
│   └── quote_fetcher.py     # Quote fetching from API
├── tests/                   # Test directory
│   ├── __init__.py
│   ├── test_quote_sender.py
│   ├── test_email_handler.py
│   └── test_quote_fetcher.py
├── quotes.json              # Local quotes database
├── requirements.txt         # Project dependencies
├── setup.py                # Package setup file
└── README.md
```

### Dependencies
requests

### Environment Variables
Required environment variables:

- SMTP_SERVER
- SMTP_PORT
- SMTP_LOGIN
- SMTP_PASSWORD

### Error Handling

The application handles the following error cases:

- Missing or invalid email addresses
- Invalid JSON file format
- Non-existent files
- Invalid command-line arguments
- API connection errors

### Testing
Run the test suite:

unittest
Tests use mocks to avoid sending actual emails and making API calls during testing.

`python -m unittest tests/test_send_inspiration.py`
