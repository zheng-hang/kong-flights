from flask import Flask, jsonify, request  
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ, path

seat_queue_name = environ.get('seat_queue_name') or 'SeatUpdate'
# seat_queue_name = 'SeatUpdate'

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3313/seats_db' # Replace with your database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
CORS(app)

db = SQLAlchemy(app)

class Seats(db.Model):
    __tablename__ = 'seats'

    # CHANGE ACCORDINGLY TO YOUR DATABASE SCHEMA --ray

    fid = db.Column(db.String(255), primary_key=True)
    seatcol = db.Column(db.String(1), primary_key=True)
    seatnum = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seat_class = db.Column(db.String(255), nullable=False)

    def __init__(self,fid, seatcol, seatnum, available, price, seat_class):
        self.fid = fid
        self.seatcol = seatcol
        self.seatnum = seatnum
        self.available = available
        self.price = price
        self.seat_class = seat_class

    def json(self):
        return {"fid": self.fid, "seatcol": self.seatcol, "seatnum": self.seatnum, "available": self.available, "price": self.price, "seat_class": self.seat_class}

# for SCENARIO 2 reserve seat
@app.route("/reserveseat", methods=['PUT'])
def reserveSeat():
    print("updating db")
    seat = request.json
    fid = seat.get('fid', None)
    seatcol = seat.get('seatcol', None)
    seatnum = seat.get('seatnum', None)

    seatToUpdate = Seats.query.filter_by(fid=fid, seatcol=seatcol, seatnum=seatnum).first()

    if seatToUpdate and seatToUpdate.available == True:
        try:
            print(seat)
            print(seatToUpdate)
            seatToUpdate.available = not seatToUpdate.available
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "message": f"Updated seat '{seatcol}' '{seatnum}' to {'available' if seatToUpdate.available else 'unavailable'}",
                    "data": seatToUpdate.json()
                }
            ), 200
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating booking. " + str(e)
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "seat": seat
                },
                "message": "Seat not found."
            }
        ), 404

# for SCENARIO 12 reserve seat
@app.route("/updateseat", methods=['PUT'])
def updateSeat():
    print("updating db")
    seat = request.json
    fid = seat.get('fid', None)
    seatcol = seat.get('seatcol', None)
    seatnum = seat.get('seatnum', None)

    seatToUpdate = Seats.query.filter_by(fid=fid, seatcol=seatcol, seatnum=seatnum).first()

    if seatToUpdate:
        try:
            print(seat)
            print(seatToUpdate)
            seatToUpdate.available = not seatToUpdate.available
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "message": f"Updated seat '{seatcol}' '{seatnum}' to {'available' if seatToUpdate.available else 'unavailable'}",
                    "data": seatToUpdate.json()
                }
            ), 200
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating booking. " + str(e)
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "seat": seat
                },
                "message": "Seat not found."
            }
        ), 404
    
# Get all seats
@app.route("/seat", methods=['GET'])
def get_all():
    seats = db.session.scalars(db.select(Seats)).all()
    seats = [seat.json() for seat in seats]
    if len(seats):
        return jsonify(
            {
                "code":200,
                "data": seats
            }
        )
    return jsonify(
        {
            "code":404,
            "message":"There are no seats."
        }
    ), 404


# Get all seats for flight
@app.route("/seat/<string:fid>", methods=['GET'])
def get_seat(fid):
    seats = db.session.scalars(db.select(Seats).filter_by(fid=fid)).all()
    if seats:
        return jsonify(
            {
                "code":200,
                "data": [seat.json() for seat in seats]
            }
        )
    return jsonify(
        {
            "code":404,
            "data":{
                "fid": fid
            },
            "message":"Seat not found."
        }
    ), 404


# {
#     "SQ 123": [{'seatcol':"A", 'seatnum':1}],
#     "SQ 124": [{'seatcol':"A", 'seatnum':1}]
# }


# Insert seats into Seat
@app.route('/insert_seats', methods=['POST'])
def insert_seats():
    try:
        data = request.json
        for flight, seats in data.items():
            for seat in seats:
                seat_obj = Seats(fid=flight, seatcol=seat['seatcol'], seatnum=seat['seatnum'], available=True, price=0, seat_class='economy')
                db.session.add(seat_obj)
        db.session.commit()
        return jsonify({'message': 'Seats inserted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to insert seats', 'error': str(e)}), 500


if __name__ == "__main__":
    print("This is flask for " + path.basename(__file__) + ": manage seats ...")
    app.run(host='0.0.0.0', port=5000, debug=True)


# situation where 2 is selecting the same seat hence need to reseve the seat first