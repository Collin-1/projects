import requests
import os
from datetime import datetime

# Base URL for GitHub API
BASE_URL = "https://api.github.com/"


def parse_date(date):
    """Convert date strings into datetime objects"""
    
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD date format")


def is_date_within_range(pull_request, start_date, end_date):
    """Check if a pull request's dates fall within a specified range"""

    created_at = parse_date(pull_request["created_at"][:10])
    updated_at = parse_date(pull_request["updated_at"][:10])
    closed_at = pull_request["closed_at"]
    merged_at = pull_request["merged_at"]
    last_action_date = None
    if merged_at:
        last_action_date = parse_date(merged_at[:10])
    elif closed_at:
        last_action_date = parse_date(closed_at[:10])
    else:
        last_action_date = updated_at

    return (
        start_date <= created_at <= end_date
        or start_date <= last_action_date <= end_date
    )


def get_headers():
    """Get headers for GitHub API requests, including authorization token if available"""

    token = os.getenv("GITHUB_TOKEN")
    return {"Authorization": f"token {token}"} if token else {}


def validate_owner(owner):
    """Validate if the GitHub organization exists"""

    response = requests.get(f"{BASE_URL}orgs/{owner}")
    if response.status_code == 404:
        raise ValueError(f"Repository owner {owner} not found")


def validate_repo(owner, repo):
    """Validate if the GitHub repository exists"""

    headers = get_headers()
    response = requests.get(f"{BASE_URL}repos/{owner}/{repo}", headers=headers)
    if response.status_code == 401 and headers:
        raise ValueError(
            f"The provided Github token {headers["Authorization"]} is not valid"
        )
    if response.status_code == 404:
        raise ValueError(f"Repository {repo} not found")


def get_requests_within_date_range(owner, repo, start_date, end_date):
    """get pull requests within a specified date range"""

    headers = get_headers()
    params = {"state": "all", "per_page": 100}
    url = f"{BASE_URL}repos/{owner}/{repo}/pulls"
    pull_requests = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.headers["X-RateLimit-Remaining"] == "0":
            raise ValueError("API rate limit exeeded")
        for pull_request in response.json():
            if is_date_within_range(pull_request, start_date, end_date):
                pull_request["created_at"] = pull_request["created_at"].split("T")[0]
                pull_requests.append(pull_request)
        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            break

    return pull_requests


def get_pull_requests(owner: str, repo: str, start_date: str, end_date: str) -> list:
    """get pull requests within a date range for a specific repository"""

    validate_owner(owner)
    validate_repo(owner, repo)

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    pull_requests = get_requests_within_date_range(owner, repo, start_date, end_date)
    keys = ("id", "user", "title", "state", "created_at")
    return [
        {
            key: (pull_request[key]["login"] if key == "user" else pull_request[key])
            for key in keys
        }
        for pull_request in pull_requests
    ]
