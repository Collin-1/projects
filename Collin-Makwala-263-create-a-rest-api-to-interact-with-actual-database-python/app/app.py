from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///mydatabase.db"
db = SQLAlchemy(app)


class HardDriveType(Enum):
    SSD = "SSD"
    HDD = "HDD"


class FormFactor(Enum):
    DESKTOP = "DESKTOP"
    LAPTOP = "LAPTOP"


class Computer(db.Model):
    __tablename__ = "computers"

    id = db.Column(db.Integer, primary_key=True)
    hard_drive_type = db.Column(db.Enum(HardDriveType), nullable=False)
    processor = db.Column(db.String(50), nullable=False)
    amount_of_ram = db.Column(db.Integer, nullable=False)
    maximum_ram = db.Column(db.Integer, nullable=False)
    hard_drive_space = db.Column(db.Integer, nullable=False)
    form_factor = db.Column(db.Enum(FormFactor), nullable=False)

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


def create_table():
    with app.app_context():
        db.create_all()


@app.route("/umuzi/api/computers", methods=["GET"])
def list_all_computers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Computer.query.paginate(page=page, per_page=per_page)
    computers = pagination.items

    return jsonify([computer.serialize() for computer in computers]), 200


@app.route("/umuzi/api/computers", methods=["POST"])
def add_computer():
    data = request.json
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


@app.route("/umuzi/api/computers/<int:id>", methods=["PUT"])
def edit_computer(id):
    old_computer = db.session.get(Computer, id)
    if not old_computer:
        return jsonify({"message": "computer not found!"}), 404
    new_info = request.get_json()
    old_computer.hard_drive_type = new_info["hard_drive_type"]
    old_computer.processor = new_info["processor"]
    old_computer.amount_of_ram = new_info["amount_of_ram"]
    old_computer.maximum_ram = new_info["maximum_ram"]
    old_computer.hard_drive_space = new_info["hard_drive_space"]
    old_computer.form_factor = new_info["form_factor"]
    db.session.commit()
    return jsonify({"message": "computer updated!"}), 200


@app.route("/umuzi/api/computers/<int:id>", methods=["DELETE"])
def delete_computer(id):
    computer = db.session.get(Computer, id)
    if not computer:
        return jsonify({"message": "computer not found!"}), 404
    db.session.delete(computer)
    db.session.commit()
    return jsonify({"message": "computer deleted!"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
