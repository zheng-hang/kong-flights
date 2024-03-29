#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import amqp_connection
import json
import pika
from os import environ

booking_queue_name = environ.get('avail_queue_name') or 'BookingUpdate'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Bookings(db.Model):
    __tablename__ = 'bookings'

    bid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, nullable=False)
    fid = db.Column(db.String(6), nullable=False)
    seatcol = db.Column(db.String(1), nullable=False)
    seatnum = db.Column(db.Integer, nullable=False)

    def __init__(self, pid, fid, seatcol, seatnum):
        self.pid = pid
        self.fid = fid
        self.seatcol = seatcol
        self.seatnum = seatnum

    def json(self):
        return {"bid": self.bid, "pid": self.pid, "fid": self.fid, "seatcol": self.seatcol, "seatnum": self.seatnum}



# Receive seat change
def receiveUpdateLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=booking_queue_name, on_message_callback=callback, auto_ack=True)
        print('bookings: Consuming from queue:', booking_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"bookings: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("bookings: Program interrupted by user.")


# Run function based on the message
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nbookings: Received an update by " + __file__)
    message = json.loads(body)
    if 'seatno' in message:
        processUpdate(message)
    elif 'pid' in message and 'fid' in message and 'seatcol' in message and 'seatno' in message:
        processCreation(message)
    else:
        print("bookings: Unknown message format")
    print()

## FORMAT FOR BODY - Update Seat    ##
## Routing Key: #.seatUpdate             ##
# {
#     "bid",
#     "seatcol": "A",
#     "seatno": 1
# }

def processUpdate(update):
    print("bookings: Recording an update:")
    print(update)
    
    # Retrieve the bid from the update
    bid = update.get('bid')

    # Retrieve the seatcol and seatnum from the update
    seatcol = update.get('seatcol')
    seatnum = update.get('seatno')  # 'seatno' in the message, update to match the key used in the message

    # Query the database for the booking with the given bid
    booking = Bookings.query.filter_by(bid=bid).first()

    if booking:
        # Update the seatcol and seatnum for the booking
        booking.seatcol = seatcol
        booking.seatnum = seatnum
        db.session.commit()
        print(f"Updated seatcol to '{seatcol}' and seatnum to '{seatnum}' for booking with bid '{bid}'")
    else:
        print(f"Booking with bid '{bid}' not found")

## FORMAT FOR BODY - CreateBooking    ##
## Routing Key: *.newBooking          ##
# {
#     "pid": 1,
#     "fid": "SQ 123",
#     "seatcol": "A",
#     "seatno": 1
# }

def processCreation(update):
    print("bookings: Recording a creation:")
    print(update)
    booking = Bookings(pid=update['pid'], fid=update['fid'], seatcol=update['seatcol'], seatnum=update['seatno'])
    db.session.add(booking)
    db.session.commit()
    print("bookings: Recorded the creation in the database")


@app.route("/book/<int:pid>")
def search_by_pid(pid):
    bookings = db.session.query(Bookings).filter(Bookings.pid == pid).all()
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
            "message": "Bookings not found for passenger ID {}.".format(pid)
        }
    ), 404

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(host='0.0.0.0', port=5000, debug=True)

    print("bookings: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("bookings: Connection established successfully")
    channel = connection.channel()
    receiveUpdateLog(channel)

    