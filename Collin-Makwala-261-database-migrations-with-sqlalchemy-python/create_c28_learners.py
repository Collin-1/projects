from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Learner

db_url = "postgresql://user2:pass2@localhost:5433/prod"
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def create_learner(first_name, surname, rockechat_user, github_name, personal_email_address, cohort):
    learner = Learner(first_name, surname, rockechat_user, github_name, personal_email_address, cohort)

    session.add(learner)
    session.commit()
    print("added learner")

create_learner("Jane", "Doe", "J-Doe", "JaneD", "janedoe@example.com", "C28 Data Eng")
create_learner("John", "Doe", "J-Doe", "JohnD", "johndoe@example.com", "C28 Data Eng")
create_learner("Jill", "Hunter", "Jill-Hunter", "J-Hunter", "jillhunter@example.com", "C28 Data Eng")
create_learner("Blake", "Lively", "B-Live", "BLIVE", "blakelively@example.com", "C28 Data Eng")