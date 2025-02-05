from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Learner(Base):
    __tablename__ = "learner"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    rocketchat_user = Column(String, nullable=False)
    github_name = Column(String, nullable=False)
    personal_email_address = Column(String, nullable=False, unique=True)
    cohort = Column(String, nullable=False)

    def __init__(self, first_name, surname, rocketchat_user, github_name, personal_email_address, cohort):
        self.first_name = first_name
        self.surname = surname
        self.rocketchat_user = rocketchat_user
        self.github_name = github_name
        self.personal_email_address = personal_email_address
        self.cohort = cohort