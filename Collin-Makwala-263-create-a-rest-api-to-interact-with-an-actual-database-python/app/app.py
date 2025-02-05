from flask import Flask, request, jsonify # Flask for web framework, request to handle HTTP requests, jsonify to return JSON responses
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy for ORM (Object-Relational Mapping)
from enum import Enum # Enum for creating enumerated constants

app = Flask(__name__) # Initialize the Flask application

# Configure the SQLAlchemy database URI to use SQLite and store the database in a file named 'mydatabase.db'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///mydatabase.db"

db = SQLAlchemy(app) # Initialize the SQLAlchemy database with the Flask app

# Define an enumeration for hard drive types
class HardDriveType(Enum):
    SSD = "SSD"
    HDD = "HDD"

# Define an enumeration for form factors
class FormFactor(Enum):
    DESKTOP = "DESKTOP"
    LAPTOP = "LAPTOP"

# Define the Computer model that represents the 'computers' table in the database
class Computer(db.Model):
    __tablename__ = "computers" # Name of the table in the database

    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    hard_drive_type = db.Column(db.Enum(HardDriveType), nullable=False)
    processor = db.Column(db.String(50), nullable=False)
    amount_of_ram = db.Column(db.Integer, nullable=False)
    maximum_ram = db.Column(db.Integer, nullable=False)
    hard_drive_space = db.Column(db.Integer, nullable=False)
    form_factor = db.Column(db.Enum(FormFactor), nullable=False)

    # Method to serialize the Computer object into a dictionary
    def serialize(self):
        return {
            "id": self.id,
            "hard_drive_type": self.hard_drive_type.value,
            "processor": self.processor,
            "amount_of_ram": self.amount_of_ram,
            "maximum_ram": self.maximum_ram,
            "hard_drive_space": self.hard_drive_space,
            "form_factor": self.form_factor.value,
        }

# Function to create the database tables
def create_table():
    with app.app_context():
        db.create_all()

# Route to list all computers with pagination support
@app.route("/umuzi/api/computers", methods=["GET"])
def list_all_computers():
    """Get pagination parameters from the query string, defaulting to page 1 and 10 items per page"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Computer.query.paginate(page=page, per_page=per_page)
    computers = pagination.items

    # Return the serialized list of computers as a JSON response
    return jsonify([computer.serialize() for computer in computers]), 200


# Route to add a new computer
@app.route("/umuzi/api/computers", methods=["POST"])
def add_computer():
    data = request.json

    # Validate the hard drive type
    if data["hard_drive_type"] not in HardDriveType:
        return (
            jsonify(
                {
                    "message": f"Invalid hard drive type. Allowed values are {list(HardDriveType.__members__.keys())}."
                }
            ),
            406,
        )
    if data["form_factor"] not in FormFactor:
        return (
            jsonify(
                {
                    "message": f"Invalid form factor. Allowed values are {list(FormFactor.__members__.keys())}."
                }
            ),
            406,
        )
    new_computer = Computer(**request.json)
    db.session.add(new_computer)
    db.session.commit()
    return jsonify(new_computer.serialize()), 201


# Route to edit an existing computer by ID
@app.route("/umuzi/api/computers/<int:id>", methods=["PUT"])
def edit_computer(id):

    # Retrieve the computer from the database by ID
    old_computer = db.session.get(Computer, id)
    if not old_computer:
        return jsonify({"message": "computer not found!"}), 404
    
    # Get the new information from the request body
    new_info = request.get_json()
    
    old_computer.hard_drive_type = new_info["hard_drive_type"]
    old_computer.processor = new_info["processor"]
    old_computer.amount_of_ram = new_info["amount_of_ram"]
    old_computer.maximum_ram = new_info["maximum_ram"]
    old_computer.hard_drive_space = new_info["hard_drive_space"]
    old_computer.form_factor = new_info["form_factor"]
    db.session.commit()
    return jsonify({"message": "computer updated!"}), 200


# Route to delete a computer by ID
@app.route("/umuzi/api/computers/<int:id>", methods=["DELETE"])
def delete_computer(id):

    # Retrieve the computer from the database by ID
    computer = db.session.get(Computer, id)
    if not computer:
        return jsonify({"message": "computer not found!"}), 404
    db.session.delete(computer)
    db.session.commit()
    return jsonify({"message": "computer deleted!"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
