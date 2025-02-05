# Import  testing and application modules
import json

import pytest

from app.app import app, db

# Fixture to set up the test client and database
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


# Fixture to provide a sample desktop computer data
@pytest.fixture
def desktop_computer():
    return {
        "hard_drive_type": "SSD",
        "processor": "Intel i7",
        "amount_of_ram": 16,
        "maximum_ram": 64,
        "hard_drive_space": 1000,
        "form_factor": "DESKTOP",
    }


# Test to list all computers and check if the response is a list
def test_list_all_computers(client):
    response = client.get("umuzi/api/computers")
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)


# Test to add a new computer and check if it is added successfully
def test_add_computer(client, desktop_computer):
    computer = desktop_computer
    response = client.post("/umuzi/api/computers", json=computer)
    assert response.status_code == 201
    assert "id" in json.loads(response.data)


# Test to add a computer with an invalid form factor and check for the appropriate error message
def test_add_computer_invalid_enum(client):
    computer = {
        "hard_drive_type": "HDD",
        "processor": "Intel i5",
        "amount_of_ram": 8,
        "maximum_ram": 32,
        "hard_drive_space": 500,
        "form_factor": "TABLET",
    }
    response = client.post(f"umuzi/api/computers", json=computer)
    assert response.status_code == 406
    assert (
        json.loads(response.data)["message"]
        == "Invalid form factor. Allowed values are ['DESKTOP', 'LAPTOP']."
    )

# Test to edit an existing computer and check if it is updated successfully
def test_edit_computer(client, desktop_computer):
    computer = desktop_computer
    response = client.post("umuzi/api/computers", json=computer)
    computer_id = json.loads(response.data)["id"]

    updated_computer = {
        "hard_drive_type": "HDD",
        "processor": "Intel i5",
        "amount_of_ram": 8,
        "maximum_ram": 32,
        "hard_drive_space": 500,
        "form_factor": "LAPTOP",
    }

    response = client.put(f"umuzi/api/computers/{computer_id}", json=updated_computer)
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "computer updated!"

# Test to edit a non-existent computer and check for the appropriate error message
def test_edit_nonexistent_computer(client, desktop_computer):
    computer = desktop_computer
    response = client.put("/umuzi/api/computers/9999", json=computer)
    assert response.status_code == 404
    assert json.loads(response.data)["message"] == "computer not found!"

# Test to delete an existing computer and check if it is deleted successfully
def test_delete_computer(client, desktop_computer):
    computer = desktop_computer
    response = client.post("umuzi/api/computers", json=computer)
    computer_id = json.loads(response.data)["id"]
    response = client.delete(f"/umuzi/api/computers/{computer_id}")
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "computer deleted!"


# Test to delete a non-existent computer and check for the appropriate error message
def test_delete_nonexistent_computer(client):
    response = client.delete("/umuzi/api/computers/9999")
    assert response.status_code == 404
    assert json.loads(response.data)["message"] == "computer not found!"

# Test to check pagination functionality and ensure it returns the correct number of items per page
def test_pagination(client, desktop_computer):
    for _ in range(25):
        computer = desktop_computer
        response = client.post("/umuzi/api/computers", json=computer)
    response = client.get("/umuzi/api/computers?page=3")
    assert response.status_code == 200
    assert len(json.loads(response.data)) == 5
