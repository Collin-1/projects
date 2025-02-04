import os
import pymongo
from dotenv import load_dotenv

load_dotenv(".env")

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

client = pymongo.MongoClient(f"mongodb://{username}:{password}@mongo:27017")

umuzi_db = client["umuzi_prospects"]

if "visitors" in umuzi_db.list_collection_names():
    umuzi_db_collection = umuzi_db["visitors"]
else:
    umuzi_db_collection = umuzi_db.create_collection("visitors")

student_valid = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "visitor_name",
            "visitor_age",
            "date_of_visit",
            "time_of_visit",
            "name_of_assistant",
            "comments",
        ],
        "properties": {
            "visitor_name": {
                "bsonType": "string",
                "description": "'visitor_name' should be a string and is required",
            },
            "visitor_age": {
                "bsonType": "int",
                "description": "'visitor_age' should be a number and is required",
            },
            "date_of_visit": {
                "bsonType": "string",
                "description": "'date_of_visit' should be a string and is required",
            },
            "time_of_visit": {
                "bsonType": "string",
                "description": "'time_of_visit' should be a string and is required",
            },
            "name_of_assistant": {
                "bsonType": "string",
                "description": "'name_of_assistant' should be a string and is required",
            },
            "comments": {
                "bsonType": "string",
                "description": "'comments' should be a string and is required",
            },
        },
    }
}

umuzi_db.command("collMod", "visitors", validator=student_valid)
