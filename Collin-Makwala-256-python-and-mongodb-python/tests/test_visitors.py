import unittest
from unittest.mock import patch
from bson import ObjectId
from visitors.visitors import (
    create_visitor,
    list_visitors,
    delete_visitor,
    update_visitor,
    visitor_details,
    delete_all,
    student_collection,
)


class TestVisitors(unittest.TestCase):
    @patch.object(student_collection, "insert_one")
    def test_create_visitor(self, mock_insert_one):
        visitor_data = {
            "visitor_name": "Collin Makwala",
            "visitor_age": 25,
            "date_of_visit": "2023-05-20",
            "time_of_visit": "14:30",
            "name_of_assistant": "Alice",
            "comments": "Friendly",
        }
        create_visitor(*(value for value in visitor_data.values()))
        mock_insert_one.assert_called_once_with(visitor_data)

    @patch.object(student_collection, "find")
    def test_list_visitors(self, mock_find):
        mock_find.return_value = [
            {"_id": ObjectId("60d5ec9f1c9d440000d01234"), "visitor_name": "Collin Makwala"},
            {"_id": ObjectId("60d5ec9f1c9d440000d01235"), "visitor_name": "Jane Doe"},
        ]
        result = list_visitors()
        self.assertEqual(len(result), 2)

    @patch.object(student_collection, "delete_one")
    def test_delete_visitor(self, mock_delete_one):
        visitor_id = ObjectId("60d5ec9f1c9d440000d01234")
        delete_visitor(visitor_id)
        mock_delete_one.assert_called_once_with({"_id": visitor_id})

    @patch.object(student_collection, "update_one")
    def test_update_visitor(self, mock_update_one):
        visitor_id = {"_id": ObjectId("60d5ec9f1c9d440000d01234")}
        new_data = {"$set": {"visitor_name": "Updated Name"}}
        update_visitor(visitor_id, new_data)
        mock_update_one.assert_called_once_with(visitor_id, new_data)

    @patch.object(student_collection, "find_one")
    def test_visitor_details(self, mock_find_one):
        visitor_id = ObjectId("60d5ec9f1c9d440000d01234")
        mock_find_one.return_value = {
            "_id": visitor_id,
            "visitor_name": "Collin Makwala",
            "visitor_age": 25,
        }
        result = visitor_details(visitor_id)
        self.assertEqual(result["visitor_name"], "Collin Makwala")

    @patch.object(student_collection, "drop")
    def test_delete_all(self, mock_drop):
        delete_all()
        mock_drop.assert_called_once()


if __name__ == "__main__":
    unittest.main()