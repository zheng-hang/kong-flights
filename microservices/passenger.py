from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/users' # Replace with your database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

CORS(app)

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {"userid": self.id, "username": self.name, "email": self.email, "password": self.password}


@app.route('/users', methods=['GET'])
def get_all():
    users = db.session.scalars(db.select(Users)).all()
    return [user.json() for user in users]


@app.route('/register', methods=['POST'])

def register():
    try:
        data = request.get_json()

        # Perform registration logic here (e.g., save user to database)
        email = data.get('email')
        password = data.get('password')

        # Check if the username and email are unique before adding to the database
        existing_user = Users.query.filter(Users.email == email).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        # Create a new user and add to the database
        new_user = Users(email=email, password= Bcrypt().generate_password_hash(password).decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'})

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception during registration: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Perform login logic here (e.g., verify user credentials)
        email = data.get('email')
        password = data.get('password')

        # Check if the user exists in the database
        user = Users.query.filter(Users.email == email).first()
        if not user:
            print("incorrect user")
            return jsonify({'error': 'Invalid email or password'}), 400

        # Check if the password is correct
        if not Bcrypt().check_password_hash(user.password, password):
            print("incorrect password")
            return jsonify({'error': 'Invalid email or password'}), 400

        return jsonify({'message': 'Login successful'})

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception during login: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

    
if __name__ == '__main__':
    app.run(port=5000, debug=True)