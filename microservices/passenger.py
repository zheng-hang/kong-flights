from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Passenger(db.Model):
    __tablename__ = 'passenger'

    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _email = db.Column(db.String(255), nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    _salt = db.Column('salt', db.String(255), nullable=False)

    def __init__(self, email, password):
        self._email = email
        self.set_password(password)

    def json(self):
        return {
            "PID": self.pid,
            "email": self._email,
            "password": self._password
        }

    def get_email(self):
        return self._email

    def set_password(self, password):
        self._salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode(), self._salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self._password.encode())


## METHODS AND PATH FOR PASSENGER ##
@app.route("/email/<int:PID>")
def get_email(PID):
    passenger = db.session.scalars(db.select(Passenger).filter_by(pid=PID).limit(1)).first()
    if passenger:
        return jsonify(
            {
                "code": 200,
                "data": passenger.getemail()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Passenger not found."
        }
    ), 404

# JSON FORMAT #
# {
#     "email": 'emily.jones987@example.org'
#     "password": "abc123"
# }

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    passenger = Passenger.query.filter_by(_email=email).first()
    if passenger and passenger.check_password(password):
        return jsonify(
            {
                "code": 200,
                "message": "Login successful."
            }
        )
    return jsonify(
        {
            "code": 401,
            "message": "Invalid email or password."
        }
    ), 401


# JSON FORMAT #
# {
#     "email": 'emily.jones987@example.org'
#     "password": "abc123"
# }

@app.route("/create", methods=["POST"])
def new_account():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if Passenger.query.filter_by(_email=email).first():
        return jsonify(
            {
                "code": 400,
                "message": "Email already exists."
            }
        ), 400
    passenger = Passenger(email=email, password=password)
    db.session.add(passenger)
    db.session.commit()
    return jsonify(
        {
            "code": 201,
            "message": "Account created successfully."
        }
    ), 201




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)