from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True)
    repo_full_name = Column(String)
    pr_number = Column(Integer)
    title = Column(String)
    state = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    author = Column(String)
    url = Column(String)
    latest_review_timestamp = Column(DateTime, nullable=True)