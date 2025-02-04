import os
from bson import ObjectId
import pymongo
from dotenv import load_dotenv

load_dotenv(".env")

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
client = pymongo.MongoClient(f"mongodb://{username}:{password}@localhost:27017")

student_collection = client.umuzi_prospects.visitors

def create_visitor(
    name, age, date_of_visit, time_of_visit, name_of_assistant, comments
):
    visitor_dictionary = {
        "visitor_name": name,
        "visitor_age": age,
        "date_of_visit": date_of_visit,
        "time_of_visit": time_of_visit,
        "name_of_assistant": name_of_assistant,
        "comments": comments,
    }
    student_collection.insert_one(visitor_dictionary)


def list_visitors():
    return [
        {key: value for key, value in visitor.items()}
        for visitor in student_collection.find()
    ]


def delete_visitor(visitor_id):
    student_collection.delete_one({"_id": ObjectId(visitor_id)})


def update_visitor(selection, new_data):
    student_collection.update_one(selection, new_data)


def visitor_details(visitor_id):
    return student_collection.find_one({"_id": ObjectId(visitor_id)})


def delete_all():
    student_collection.drop()
