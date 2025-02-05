import os
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
import requests
import logging

from inspirational_emails.send_inspiration import (
    send_email,
    get_quote,
    get_smtp_settings,
    get_receiver_email,
    create_message,
    validate_cmd_args,
    validate_emails,
    validate_json_file,
    logger
)


def test_smtp_settings():
    return (
        "server",
        "123",
        "login",
        "password",
        "sender@example.com",
    )

def test_quote():
    return {"body": "test quote", "author": "author"}


class TestGetQuote(unittest.TestCase):

    @patch("inspirational_emails.send_inspiration.requests.get")
    def test_get_quote_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Request Error")
        mock_get.return_value = mock_response
        with self.assertRaisesRegex(requests.exceptions.RequestException, "Request Error"):
            with self.assertLogs(logger, level="ERROR") as log:
                get_quote()
        self.assertIn("ERROR:inspirational_emails.send_inspiration:Request Error", log.output)

    @patch("inspirational_emails.send_inspiration.requests.get")
    def test_get_quote(self, mock_get):
        mock_get.return_value.status_code = 200
        get_quote()
        mock_get.assert_called_once()



class TestSmtpSettings(unittest.TestCase):

    @patch.dict(
        os.environ,
        {
            "SMTP_SERVER": "server",
            "SMTP_PORT": "123",
            "SMTP_LOGIN": "login",
            "SMTP_PASSWORD": "password",
            "SENDER_EMAIL": "sender@example.com",
        },
    )
    def test_get_smtp_settings(self):
        settings = get_smtp_settings()
        expected_settings = test_smtp_settings()
        self.assertEqual(settings, expected_settings)

    def test_get_smtp_settings_not_set(self):
        with self.assertRaisesRegex(ValueError, r"smtp settings \(server, port, login, password, sender_email\) must be set\."):
            with self.assertLogs(logger, level="ERROR") as log:
                get_smtp_settings()
        self.assertIn("ERROR:inspirational_emails.send_inspiration:smtp settings (server, port, login, password, sender_email) must be set.", log.output)



class TestCmdArgsValidation(unittest.TestCase):

    def test_validate_valid_cmd_args(self):
        self.assertIsNone(validate_cmd_args(["~/email_recipients.json", "--same"]))

    def test_validate_invalid_cmd_args(self):
        test_cases = [
            (["~/email_recipients.json", "--identical"], "Behaviour must be '--same'"),
            (["~/email_recipients.json", "--same", "-extra_cmd"], r"The argument must be an email_address/path_to_json and behaviour\(--same\)")
        ]

        for args, expected_message in test_cases:
            with self.subTest(args=args):
                with self.assertRaisesRegex(ValueError, expected_message):
                    with self.assertLogs(logger, level='ERROR') as log:
                        validate_cmd_args(args)
                unescaped_message = expected_message.replace(r"\(", "(").replace(r"\)", ")")
                formatted_message = f"ERROR:inspirational_emails.send_inspiration:{unescaped_message}"
                self.assertIn(formatted_message, log.output)


class TestJsonFileValidation(unittest.TestCase):

    def test_validate_json_file_non_existent_file(self):
        with self.assertRaisesRegex(
            FileNotFoundError, r"\[Errno 2\] No such file or directory: 'file_path'"
        ):
            with self.assertLogs(logger, level="ERROR") as log:
                validate_json_file("file_path")
        self.assertIn("ERROR:inspirational_emails.send_inspiration:[Errno 2] No such file or directory: 'file_path'", log.output)

    @patch("inspirational_emails.send_inspiration.open", new_callable=mock_open)
    def test_validate_json_file_invalid_format(self, mock_file):
        test_cases = [
            ('{"invalid": "json"', "The file contains an invalid JSON"),
            ('{"invalid": "json"}', "The Json file must contain a list"),
            ('[{"invalid": "json"}]', "Each dictionary should contain 'email' and 'name' keys")
        ]

        for read_data, expected_message in test_cases:
            with self.subTest(read_data=read_data):
                mock_file.return_value.read.return_value = read_data
                with self.assertRaisesRegex(ValueError, expected_message):
                    with self.assertLogs(logger, level="ERROR") as log:
                        validate_json_file("json file")
                self.assertIn(f"ERROR:inspirational_emails.send_inspiration:{expected_message}", log.output)

    @patch("inspirational_emails.send_inspiration.json.load")
    @patch("inspirational_emails.send_inspiration.os.path.expanduser")
    @patch("inspirational_emails.send_inspiration.open")
    def test_validate_json_file_valid(self, mock_open, mock_path, mock_load):
        mock_load.return_value = [
            {"email": "collinm@gmail.com", "name": "collin"},
            {"email": "john.doe@yahoo.com", "name": "john"}
        ]
        validate_json_file("file_path")
        mock_path.assert_called_once_with("file_path")


class TestReceiverEmail(unittest.TestCase):

    @patch.object(sys, "argv", ["send_inspiration", "receiver@example.com"])
    def test_get_receiver_email(self):
        receiver_email, condition = get_receiver_email()
        self.assertEqual(
            (receiver_email, condition),
            ([{"email": "receiver@example.com", "name": None}], []),
        )

    @patch.object(sys, "argv", ["send_inspiration"])
    def test_get_receiver_email_not_supplied(self):
        with self.assertRaisesRegex(ValueError, "Please provide a reciever email"):
            with self.assertLogs(logger, level="ERROR") as log:
                get_receiver_email()
        self.assertIn('ERROR:inspirational_emails.send_inspiration:Please provide a reciever email', log.output)

    def test_validate_emails_valid_email(self):
        self.assertIsNone(
            validate_emails(
                [{"email": "collinm@gmail.com"}, {"email": "john.doe@yahoo.com"}]
            )
        )

    def test_validate_emails_invalid_email(self):
        with self.assertRaisesRegex(
            ValueError, f"The reciever email, john.doe#yahoo.com, is not valid"
        ):
          with self.assertLogs(logger, level="ERROR") as log:
                validate_emails([{"email": "collinm@gmail.com"}, {"email": "john.doe#yahoo.com"}])
        self.assertIn('ERROR:inspirational_emails.send_inspiration:The reciever email, john.doe#yahoo.com, is not valid', log.output)


class TestCreateMessage(unittest.TestCase):

    @patch("inspirational_emails.send_inspiration.get_smtp_settings")
    def test_create_message(self, mock_get_smtp_settings):
        mock_get_smtp_settings.return_value = test_smtp_settings()
        quote = {"body": "test quote", "author": "author"}
        receiver_email = {"email": "receiver@example.com", "name": "Collin"}
        message = create_message(quote, receiver_email)
        self.assertEqual(message["Subject"], "Inpirational quote")
        self.assertEqual(message["From"], "sender@example.com")
        self.assertEqual(message["To"], "receiver@example.com")
        self.assertEqual(message.get_payload(), 'Dear Collin,\n\n"test quote" - author')


class TestSendEmail(unittest.TestCase):

    @patch("inspirational_emails.send_inspiration.get_smtp_settings")
    @patch("inspirational_emails.send_inspiration.get_receiver_email")
    @patch("inspirational_emails.send_inspiration.get_quote")
    @patch("inspirational_emails.send_inspiration.create_message")
    def test_send_email(
        self,
        mock_create_message,
        mock_get_quote,
        mock_get_receiver_email,
        mock_get_smtp_settings,
    ):
        mock_get_smtp_settings.return_value = test_smtp_settings()
        mock_get_receiver_email.return_value = (
            [{"email": "receiver@example.com", "name": None}],
            [],
        )
        mock_get_quote.return_value = test_quote()

        mock_message = MagicMock()
        mock_create_message.return_value = mock_message

        with patch("smtplib.SMTP") as smtp_call:
            mock_server = MagicMock()
            smtp_call.return_value.__enter__.return_value = mock_server
            with self.assertLogs(logger, level="INFO") as log:
                send_email()
                self.assertIn("INFO:inspirational_emails.send_inspiration:email sent to ['receiver@example.com']", log.output)

        smtp_call.assert_called_once_with("server", "123")
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("login", "password")
        mock_server.sendmail.assert_called_once_with(
            "sender@example.com",
            "receiver@example.com",
            mock_message.as_string.return_value,
        )


if __name__ == "__main__":
    unittest.main()
