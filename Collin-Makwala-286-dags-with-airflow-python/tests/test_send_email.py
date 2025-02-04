import unittest
from unittest.mock import patch, MagicMock
from email.mime.text import MIMEText
import os

# Import your functions
from dags.send_email import get_smtp_settings, create_message, send_email

class TestEmailFunctions(unittest.TestCase):
    def setUp(self):
        # Setup mock environment variables
        self.env_vars = {
            "SMTP_SERVER": "smtp.gmail.com",
            "SMTP_PORT": "587",
            "SMTP_LOGIN": "test@gmail.com",
            "SMTP_PASSWORD": "test_password",
            "SENDER_EMAIL": "sender@gmail.com",
            "RECEIVER_EMAIL": "receiver@gmail.com"
        }
        
    @patch.dict(os.environ, {}, clear=True)
    def test_get_smtp_settings_missing_values(self):
        """Test if ValueError is raised when environment variables are missing"""
        with self.assertRaises(ValueError):
            get_smtp_settings()

    @patch.dict(os.environ)
    def test_get_smtp_settings_success(self):
        """Test successful retrieval of SMTP settings"""
        # Set environment variables
        os.environ.update(self.env_vars)
        
        # Get settings
        result = get_smtp_settings()
        
        # Assert results
        self.assertEqual(result, (
            self.env_vars["SMTP_SERVER"],
            self.env_vars["SMTP_PORT"],
            self.env_vars["SMTP_LOGIN"],
            self.env_vars["SMTP_PASSWORD"],
            self.env_vars["SENDER_EMAIL"],
            self.env_vars["RECEIVER_EMAIL"]
        ))

    @patch('dags.send_email.get_smtp_settings')
    @patch('dags.send_email.get_top_5_pull_requests')
    def test_create_message(self, mock_get_prs, mock_get_settings):
        """Test message creation"""
        # Mock return values
        mock_get_settings.return_value = (
            "smtp.gmail.com", "587", "login", "password",
            "sender@gmail.com", "receiver@gmail.com"
        )
        mock_get_prs.return_value = "PR1\nPR2\nPR3\nPR4\nPR5"

        # Create message
        message = create_message()

        # Assert message properties
        self.assertIsInstance(message, MIMEText)
        self.assertEqual(message["From"], "sender@gmail.com")
        self.assertEqual(message["To"], "receiver@gmail.com")
        self.assertEqual(message["Subject"], "Top 5 Pull Request Reviews for the day")
        self.assertIn("PR1", message.get_payload())

    @patch('smtplib.SMTP')
    @patch('dags.send_email.get_smtp_settings')
    @patch('dags.send_email.create_message')
    def test_send_email(self, mock_create_message, mock_get_settings, mock_smtp):
        """Test email sending"""
        # Mock return values
        mock_get_settings.return_value = (
            "smtp.gmail.com", "587", "login", "password",
            "sender@gmail.com", "receiver@gmail.com"
        )
        
        mock_message = MIMEText("Test message")
        mock_message["From"] = "sender@gmail.com"
        mock_message["To"] = "receiver@gmail.com"
        mock_message["Subject"] = "Test Subject"
        mock_create_message.return_value = mock_message

        # Create mock SMTP instance
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        # Send email
        send_email()

        # Assert SMTP calls
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with("login", "password")
        mock_smtp_instance.sendmail.assert_called_once_with(
            "sender@gmail.com",
            "receiver@gmail.com",
            mock_message.as_string()
        )

if __name__ == '__main__':
    unittest.main()