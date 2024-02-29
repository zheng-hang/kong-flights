from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/your_database' # Replace with your database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        self.password = generate_password_hash(password).decode('utf-8')

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
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check if the username and email are unique before adding to the database
        existing_user = Users.query.filter((Users.name == username) | (Users.email == email)).first()
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        # Create a new user and add to the database
        new_user = Users(name=username, email=email, password= Bcrypt().generate_password_hash(password).decode('utf-8'))
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
            return jsonify({'error': 'Invalid email or password'}), 400

        # Check if the password is correct
        if not Bcrypt().check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 400

        return jsonify({'message': 'Login successful'})

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Exception during login: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

    
if __name__ == '__main__':
    app.run(port=5000, debug=True)



# Step 2: Integrate Flask Microservice with the API Gateway
# Ensure your API Gateway (Kong, custom Node.js API Gateway, etc.) is configured to route requests to the Flask microservice. You'll need to add a new route and service in Kong or configure the proxy settings in your custom API Gateway to point to your Flask service's host and port.

# For example, if using Kong:

# Add your Flask microservice as a new service in Kong.
# Configure a route in Kong that forwards to the /users endpoint of your Flask app.