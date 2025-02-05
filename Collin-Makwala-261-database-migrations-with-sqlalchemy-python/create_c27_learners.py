from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Learner


db_url = "postgresql://user2:pass2@localhost:5433/prod"
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def create_learner(first_name, surname, rockechat_user, github_name, id_number, personal_email_address, cohort):
    learner = Learner(first_name, surname, rockechat_user, github_name, id_number, personal_email_address, cohort)

    session.add(learner)
    session.commit()
    print("added learner")

create_learner("Alice", "Johnson", "A-J", "AliceJ", "76543210988", "alicejohnson@example.com", "C27 Data Eng")
create_learner("Bob", "Brown", "B-Brown", "BobB", "65432109877", "bobbrown@example.com", "C27 Data Eng")
create_learner("Emily", "Clark", "E-Clark", "EmilyC", "54321098766", "emilyclark@example.com", "C27 Data Eng")
create_learner("David", "Lee", "D-Lee", "DavidL", "43210987655", "davidlee@example.com", "C27 Data Eng")
create_learner("Sophia", "Martinez", "S-Martinez", "SophiaM", "32109876544", "sophiamartinez@example.com", "C27 Data Eng")