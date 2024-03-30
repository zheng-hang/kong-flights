import threading
from flask import Flask, jsonify, request  
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import amqp_connection
import json
import pika
from os import environ

# seat_queue_name = environ.get('seat_queue_name') or 'SeatUpdate'
seat_queue_name = 'SeatUpdate'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3313/seats_db' # Replace with your database connection string
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
CORS(app)

db = SQLAlchemy(app)

class Seats(db.Model):
    __tablename__ = 'seats'

    # CHANGE ACCORDINGLY TO YOUR DATABASE SCHEMA --ray

    fid = db.Column(db.String(255), primary_key=True)
    seatcol = db.Column(db.String(1), nullable=False)
    seatnum = db.Column(db.Integer, nullable=False)
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


# receive seat from booking
def receiveSeat(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=seat_queue_name, on_message_callback=callback, auto_ack=True)
        print('seats: Consuming from queue:', seat_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"seats: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("seats: Program interrupted by user.")

def callback(channel, method, properties, body):
    print("\nseats: Received an update by " + __file__)
    message = json.loads(body)
    if 'fid' in message:
        seat = db.session.scalars(db.select(Seats).filter_by(fid=message['fid']).limit(1)).first()
        if seat:
            seat.available = False
            db.session.commit()
            print("seats: Seat updated successfully.")
        else:
            print("seats: Seat not found.")
    else:
        print("seats: Invalid message format.")


def updateDatabase(message):
    fid = message['fid']
    seatcol = message['seatcol']
    seatnum = message['seatnum']
    available = message['available']
    price = message['price']
    seat_class = message['seat_class']
    # get the seat with the fid
    seat = db.session.scalars(db.select(Seats).filter_by(fid=fid,seatcol=seatcol, seatnum=seatnum).limit(1)).first()
    if seat:
        seat.available = not seat.available
        db.session.commit()
        print("seats: Seat updated successfully.")
    else:
        print(f"seats: Seat not found. fid  = {fid}, seatcol = {seatcol}, seatnum = {seatnum}")



@app.route("/seat", methods=['GET'])
def get_all():
    seat = db.session.scalars(db.select(Seats)).all()
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

@app.route("/seat/<string:fid>", methods=['GET'])
def get_seat(fid):
    seat = db.session.scalars(db.select(Seats).filter_by(fid=fid).limit(1)).first()
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
                "fid": fid
            },
            "message":"Seat not found."
        }
    ), 404

def start_flask():
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        print("Flask thread exiting")

def start_amqp():
    try:
        print("bookings: Getting Connection")
        connection = amqp_connection.create_connection()  # get the connection to the broker
        print("bookings: Connection established successfully")
        channel = connection.channel()
        receiveSeat(channel)
    finally:
        print("AMQP thread exiting")
    


if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    amqp_thread = threading.Thread(target=start_amqp)

    flask_thread.start()
    amqp_thread.start()
    
    try:
        flask_thread.join()
        amqp_thread.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting threads")