#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import amqp_connection
import pika
from os import environ, path

booking_queue_name = environ.get('avail_queue_name') or 'BookingUpdate'
exchangename = environ.get('exchangename') or 'notif_topic'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@host.docker.internal:3312/bookings_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
#booking
db = SQLAlchemy(app)

CORS(app)

class Bookings(db.Model):
    __tablename__ = 'bookings'

    bid = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    fid = db.Column(db.String(6), nullable=False)
    seatcol = db.Column(db.String(1), nullable=False)
    seatnum = db.Column(db.Integer, nullable=False)

    def __init__(self, email, fid, seatcol, seatnum):
        self.email = email
        self.fid = fid
        self.seatcol = seatcol
        self.seatnum = seatnum

    def json(self):
        return {"bid": self.bid, "email": self.email, "fid": self.fid, "seatcol": self.seatcol, "seatnum": self.seatnum}



# connection = amqp_connection.create_connection() 
# channel = connection.channel()


## FORMAT FOR BODY - CreateBooking    ##
## Routing Key: *.newBooking          ##
# {
#     "email": "pain@gmail.com"
#     "fid": "SQ 123",
#     "seatcol": "A",
#     "seatnum": 1
# }


@app.route("/newbooking", methods=['POST'])
def processCreationReq():
    print("bookings: Recording a creation:")
    
    print(request.json)
    booking = Bookings(email=request.json.get('email', None), 
                       fid=request.json.get('fid', None), 
                       seatcol=request.json.get('seatcol', None), 
                       seatnum=request.json.get('seatnum', None))
    try:
        db.session.add(booking)
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": booking.json()
            }), 201
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the booking. " + str(e)
            }
        ), 500
    
    message =   json.dumps(booking.json())
    message['source'] = "bookings"
    print(message)

    # channel.basic_publish(exchange=exchangename, routing_key="bookingupdate.notif", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    # return jsonify(
    #     {
    #         "code": 201,
    #         "data": booking.json()
    #     }
    # ), 201



@app.route("/update", methods=['PUT'])
def processUpdateReq():
    print("bookings: Recording a update:")

    update = request.json
    print(update)

    # Retrieve the bid from the update
    bid = update.get('bid')
    seatcol = update.get('seatcol')
    seatnum = update.get('seatnum')

    booking = Bookings.query.filter_by(bid=bid).first()

    if booking:
        try:
            # Update the seatcol and seatnum for the booking
            booking.seatcol = seatcol
            booking.seatnum = seatnum
            db.session.commit()

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
                "message": f"Booking with bid '{bid}' not found"
            }
        ), 404

    # booking_updated = Bookings.query.filter_by(bid=bid).first()
    # message = json.dumps(booking_updated.json())

    # channel.basic_publish(exchange=exchangename, routing_key="bookingupdate.notif", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    
    return jsonify(
    {
        "code": 200,
        "message": f"Updated booking with bid '{bid}' to seat '{seatcol}' '{seatnum}'",
        "data": booking.json()
    }), 200



@app.route("/booking/<string:email>")
def search_by_email(email):
    bookings = db.session.query(Bookings).filter(Bookings.email == email).all()
    if bookings:
        # Convert each booking to a dictionary using the json method
        data = [booking.json() for booking in bookings]
        return jsonify(
            {
                "code": 200,
                "data": data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Bookings not found for passenger ID {}.".format(email)
        }
    ), 404

@app.route("/booking/<int:bid>")
def search_by_bid(bid):
    booking = db.session.query(Bookings).filter(Bookings.bid == bid).first()
    if booking:
        return jsonify(
            {
                "code": 200,
                "data": booking.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Booking not found for booking ID {}.".format(bid)
        }
    ), 404

@app.route("/booking")
def get_all():
    bookings = db.session.query(Bookings).all()
    if bookings:
        data = [booking.json() for booking in bookings]
        return jsonify(
            {
                "code": 200,
                "data": data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bookings."
        }
    ), 404
    

if __name__ == "__main__":
    print("This is flask for " + path.basename(__file__) + ": manage bookings ...")
    app.run(host='0.0.0.0', port=5000, debug=True)

    