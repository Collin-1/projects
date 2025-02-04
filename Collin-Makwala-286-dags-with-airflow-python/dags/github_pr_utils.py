import os
from datetime import datetime

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import PullRequest, Base

import requests


BASE_URL = "https://api.github.com"
Token = os.getenv("GITHUB_TOKEN")

s = requests.Session()
s.headers.update({"Authorization": f"token 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"})

def parse_github_datetime(dt_str):
    if not dt_str:
        return None
    return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")


def get_db_session():
    db_connection_string = (
        "postgresql://airflow:airflow@localhost/airflow"  # os.getenv("DATABASE_URL")
    )
    engine = create_engine(db_connection_string)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


def get_all_repos():
    all_repos = []
    page = 1
    while True:
        response = s.get(
            f"{BASE_URL}/user/repos", params={"page": page, "per_page": 100}
        )

        response.raise_for_status()
        repos = response.json()
        if not repos:
            break
        all_repos.extend(repos)
        page += 1
    return all_repos


def get_open_pr():
    all_repos = get_all_repos()
    all_open_pull_requests = []

    for repo in all_repos:

        repo_name = repo["full_name"]

        try:
            open_pull_requests = s.get(
                f"{BASE_URL}/repos/{repo_name}/pulls", params={"state": "open"}
            ).json()
        except requests.exceptions.RequestException as e:
            raise e
        for open_pr in open_pull_requests:
            open_pr["repo_full_name"] = repo_name
            all_open_pull_requests.append(open_pr)

    return all_open_pull_requests


def insert_data_to_database():
    session = get_db_session()

    pull_requests = get_open_pr()

    for pull_request in pull_requests:
        pull_request = PullRequest(
            repo_full_name=pull_request["repo_full_name"],
            pr_number=pull_request["number"],
            title=pull_request["title"],
            state=pull_request["state"],
            created_at=parse_github_datetime(pull_request["created_at"]),
            updated_at=parse_github_datetime(pull_request["updated_at"]),
            author=pull_request["user"]["login"],
            url=pull_request["html_url"],
        )

        session.add(pull_request)

    session.commit()



def get_latest_review_timestamp():
    session = get_db_session()
    pull_requests = session.query(PullRequest).all()

    for pr in pull_requests:
        try:
            # Get all reviews for the PR
            reviews_response = s.get(
                f"{BASE_URL}/repos/{pr.repo_full_name}/pulls/{pr.pr_number}/reviews"
            )
            reviews_response.raise_for_status()
            reviews = reviews_response.json()

            # Find the latest review timestamp
            latest_timestamp = None
            if reviews:
                latest_timestamp = max([
                    parse_github_datetime(review['submitted_at'])
                    for review in reviews
                    if review['submitted_at']
                ])

            # Update the existing PR record
            pr.latest_review_timestamp = latest_timestamp
            # No need to call session.add() since the object is already in the session

        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews for PR #{pr.pr_number} in {pr.repo_full_name}: {str(e)}")
            continue

    session.commit()

def get_top_5_pull_requests():
    session = get_db_session()
    pull_requests = session.query(PullRequest).all() 

    pr_urls = [(pr.url, pr.latest_review_timestamp) for pr in pull_requests if pr.latest_review_timestamp]
    sorted_pr_urls = sorted(pr_urls, key=lambda pr_date: pr_date[0], reverse=True)[:5]
    top_5_prs = "\n".join([f"{pr[0]}, { pr[1].strftime("%m-%d-%Y")}" for pr in sorted_pr_urls])

    return top_5_prs

# insert_data_to_database()
# get_latest_review_timestamp()