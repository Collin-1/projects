from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Learner

db_url = "postgresql://user2:pass2@localhost:5433/prod"
engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def create_learner(first_name, surname, chatname, github_name, id_number, personal_email_address, cohort):
    learner = Learner(first_name, surname, chatname, github_name, id_number, personal_email_address, cohort)

    session.add(learner)
    session.commit()
    print("added learner")


create_learner("Billy", "Bob", "b-b", "bb-1", "89324788754", "billybob@gmail.com", "C26 Data Eng")
create_learner("Paul", "Morgan", "PMorgan", "paulm", "12382044435", "paulmorgan@gmail.com", "C26 Data Eng")
create_learner("Steve", "Walker", "SWalker", "walkers", "80737720754", "stevem@gmail.com", "C26 Data Eng")
create_learner("Joe", "Norris", "JoeyN", "jn-10", "12323444435", "joenorris@gmail.com", "C26 Data Eng")
create_learner("Dexter", "Lucky", "D_luck", "DL", "89309820754", "dexterlucky@gmail.com", "C26 Data Eng")