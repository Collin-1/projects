from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Learner


db_url = "postgresql://user1:pass1@localhost:5432/development"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def create_learner(first_name, surname, chatname, github_name, id_number, personal_email_address):
    learner = Learner(first_name, surname, chatname, github_name, id_number, personal_email_address)

    session.add(learner)
    session.commit()
    print("added learner")

create_learner("Sam", "Copper", "S-Cop", "S-Cop-1", "89324720754", "samcopper@gmail.com")
create_learner("Mike", "Smith", "Mike-S", "MikeSmith", "12332444435", "mikesmith@gmail.com")