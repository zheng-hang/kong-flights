from flask import Flask, jsonify, request  
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/your_database' # Replace with your database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

class Seat(db.Model):
    __tablename__ = 'seat'

    # CHANGE ACCORDINGLY TO YOUR DATABASE SCHEMA --ray

    seat_fid = db.Column(db.Integer, primary_key=True)
    seat_col = db.Column(db.CHAR(1), nullable=False) 
    seat_num = db.Column(db.String(255), nullable=False)
    availability = db.Column(db.String(255), nullable=False)
    seat_price = db.Column(db.Float, nullable=False)
    seat_class = db.Column(db.String(255), nullable=False)

    def __init__(self,seat_fid, seat_col, seat_num, availability, seat_price, seat_class):
        self.seat_fid = seat_fid
        self.seat_col = seat_col
        self.seat_num = seat_num
        self.availability = availability
        self.seat_price = seat_price
        self.seat_class = seat_class

    def json(self):
        return {"seat_fid": self.seat_fid, "seat_col": self.seat_col, "seat_num": self.seat_num, "availability": self.availability, "seat_price": self.seat_price, "seat_class": self.seat_class}


@app.route('/seat', methods=['GET'])
def get_all():
    seat = db.session.scalars(db.select(Seat)).all()
    if len(seat):
        return jsonify(
            {
                "code":200,
                "data": [seat.json() for seat in seat]
            }
        )
    return jsonify(
        {
            "code":404,
            "message":"There are no seats."
        }
    ), 404

@app.route("/seat/<string:seat_fid", methods=['GET'])
def get_seat(seat_fid):
    seat = db.session.scalars(db.select(Seat).filter_by(seat_fid=seat_fid).limit(1)).first()
    if seat:
        return jsonify(
            {
                "code":200,
                "data": seat.json()
            }
        )
    return jsonify(
        {
            "code":404,
            "data":{
                "seat_fid": seat_fid
            },
            "message":"Seat not found."
        }
    ), 404


# assume seat is selected by user
@app.route("/seat/select/<string:seat_fid>", methods=['PUT'])
def select_seat(seat_fid):
    seat = db.session.scalars(db.select(Seat).filter_by(seat_fid=seat_fid).limit(1)).first()
    if seat:
        seat.availability = "Unavailable"
        db.session.commit()
        return jsonify(
            {
                "code":200,
                "data": seat.json()
            }
        )
    return jsonify(
        {
            "code":404,
            "data":{
                "seat_fid": seat_fid
            },
            "message":"Seat not found."
        }
    ), 404
    