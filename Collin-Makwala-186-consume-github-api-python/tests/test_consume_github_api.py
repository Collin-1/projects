# Standard library imports for unit testing
import unittest
from unittest.mock import patch, MagicMock # For mocking external dependencies in tests
from datetime import datetime # DateTime handling for date-related tests

# Import functions to be tested from the main module
from consume_github_api.consume_github_api import (
    parse_date,
    is_date_within_range,
    validate_owner,
    validate_repo,
    get_requests_within_date_range,
    get_pull_requests,
)


class TestConsume(unittest.TestCase):
    def test_parse_date(self):
        """Test that parse_date correctly converts a valid date string to a datetime object"""

        self.assertEqual(parse_date("2022-03-01"), datetime(2022, 3, 1).date())

    def test_parse_date_error(self):
        """Test that parse_date raises ValueError for invalid date format"""

        with self.assertRaises(ValueError) as cm:
            parse_date("01,03,2023")
        self.assertEqual(
            "Invalid date format. Expected YYYY-MM-DD date format", str(cm.exception)
        )

    def test_is_date_within_range(self):
        """Test that is_date_within_range correctly identifies pull requests within the specified date range"""

        pull_request = {
            "created_at": "2022-03-10T06:07:37Z",
            "updated_at": "2022-05-24T06:07:37Z",
            "closed_at": "2022-05-24T06:07:37Z",
            "merged_at": "2022-05-24T06:07:37Z",
        }
        start_date, end_date = parse_date("2022-02-20"), parse_date("2022-04-12")
        self.assertTrue(is_date_within_range(pull_request, start_date, end_date))

    @patch("requests.get")
    def test_validate_owner_found(self, mock_get):
        """Test that validate_owner returns None for valid repository owner"""

        mock_get.return_value.status_code = 200
        self.assertIsNone(validate_owner("valid_owner"), None)

    @patch("requests.get")
    def test_validate_owner_not_found(self, mock_get):
        """Test that validate_owner raises ValueError for invalid repository owner"""

        mock_get.return_value.status_code = 404
        with self.assertRaises(ValueError) as cm:
            validate_owner("invalid_owner")
        self.assertEqual("Repository owner invalid_owner not found", str(cm.exception))

    @patch("requests.get")
    def test_validate_repo_found(self, mock_get):
        """Test that validate_repo returns None for valid repository"""

        mock_get.return_value.status_code = 200
        self.assertIsNone(validate_repo("valid_owner", "valid_repo"), None)

    @patch("requests.get")
    def test_validate_repo_not_found(self, mock_get):
        """Test that validate_repo raises ValueError for invalid repository"""

        mock_get.return_value.status_code = 404
        with self.assertRaises(ValueError) as cm:
            validate_repo("valid_owner", "Invalid_repo")
        self.assertEqual("Repository Invalid_repo not found", str(cm.exception))

    @patch("requests.get")
    def test_get_requests_within_date_range(self, mock_get):
        """Test that get_requests_within_date_range returns correct pull requests within date range"""

        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "created_at": "2023-08-01T06:07:37Z",
                "updated_at": "2023-08-05T06:07:37Z",
                "closed_at": "2022-05-24T06:07:37Z",
                "merged_at": "2022-05-24T06:07:37Z",
            }
        ]
        mock_response.links.return_value = {}
        mock_get.return_value = mock_response

        start_date = parse_date("2023-8-1")
        end_date = parse_date("2023-8-10")
        pull_requests = get_requests_within_date_range(
            "owner", "repo", start_date, end_date
        )
        self.assertEqual(len(pull_requests), 1)

    @patch("consume_github_api.consume_github_api.validate_owner")
    @patch("consume_github_api.consume_github_api.validate_repo")
    @patch("consume_github_api.consume_github_api.get_requests_within_date_range")
    def test_get_pull_requests(
        self, mock_requests_within_range, mock_validate_repo, mock_validate_owner
    ):
        """Test that get_pull_requests returns correctly formatted pull request data"""

        pull_request = [
            {
                "id": 872481470,
                "number": 382,
                "state": "closed",
                "locked": False,
                "title": "Update _index.md",
                "user": {"login": "Kate-bit-dev"},
                "created_at": "2022-03-06",
                "assignee": None,
                "requested_reviewers": [],
            }
        ]
        mock_validate_owner.return_value = None
        mock_validate_repo.return_value = None
        mock_requests_within_range.return_value = pull_request

        results = get_pull_requests(
            "Umuzi-org", "ACN-syllabus", "2022-03-01", "2022-03-10"
        )
        expected_results = [
            {
                "id": 872481470,
                "state": "closed",
                "title": "Update _index.md",
                "user": "Kate-bit-dev",
                "created_at": "2022-03-06",
            }
        ]

        self.assertEqual(results, expected_results)

    @patch("requests.get")
    def test_rate_limit_hit(self, mock_get):
        """Test that API rate limit error is handled correctly"""

        mock_response = MagicMock()
        mock_response.headers = {"X-RateLimit-Remaining": "0"}
        mock_get.return_value = mock_response
        with self.assertRaises(ValueError) as cm:
            get_requests_within_date_range("owner", "repo", "2023-8-1", "2023-8-10")
        self.assertEqual("API rate limit exeeded", str(cm.exception))

    @patch("requests.get")
    def test_pull_request_outside_date_range(self, mock_get):
        """Test that pull requests outside the date range are filtered out"""

        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "created_at": "2023-08-01T06:07:37Z",
                "updated_at": "2023-08-05T06:07:37Z",
                "closed_at": "2022-05-24T06:07:37Z",
                "merged_at": "2022-05-24T06:07:37Z",
            }
        ]
        mock_response.links.return_value = {}
        mock_get.return_value = mock_response

        start_date = parse_date("2020-8-1")
        end_date = parse_date("2020-8-10")
        pull_requests = get_requests_within_date_range(
            "owner", "repo", start_date, end_date
        )
        self.assertEqual(pull_requests, [])

    @patch("requests.get")
    def test_start_date_is_after_end_date(self, mock_get):
        """Test handling of invalid date range where start date is after end date"""

        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "created_at": "2023-08-01T06:07:37Z",
                "updated_at": "2023-08-05T06:07:37Z",
                "closed_at": "2022-05-24T06:07:37Z",
                "merged_at": "2022-05-24T06:07:37Z",
            }
        ]
        mock_response.links.return_value = {}
        mock_get.return_value = mock_response

        start_date = parse_date("2023-8-10")
        end_date = parse_date("2023-8-1")
        pull_requests = get_requests_within_date_range(
            "owner", "repo", start_date, end_date
        )
        self.assertEqual(pull_requests, [])

    @patch("consume_github_api.consume_github_api.get_headers")
    @patch("requests.get")
    def test_validate_repo_with_invalid_token(self, mock_get, mock_get_headers):
        """Test that invalid GitHub token is handled correctly"""

        mock_get_headers.return_value = {"Authorization": f"token invalid_token"}
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(
            ValueError, "The provided Github token token invalid_token is not valid"
        ):
            validate_repo("valid_owner", "valid_repo")


if __name__ == "__main__":
    unittest.main()
