import threading
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from datetime import datetime

import amqp_connection
import json
import pika

flight_queue_name = environ.get('flight_queue_name') or 'FlightInsert'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Flight(db.Model):
    __tablename__ = 'flights'

    FID = db.Column(db.String(6), primary_key=True)
    Airline = db.Column(db.String(255))
    DepartureLoc = db.Column(db.String(255), nullable=False)
    ArrivalLoc = db.Column(db.String(255), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    DepartureTime = db.Column(db.Time, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, FID, Airline, DepartureLoc, ArrivalLoc, Date, DepartureTime, Duration, Price):
        self.FID = FID
        self.Airline = Airline
        self.DepartureLoc = DepartureLoc
        self.ArrivalLoc = ArrivalLoc
        self.Date = Date
        self.DepartureTime = DepartureTime
        self.Duration = Duration
        self.Price = Price

    def json(self):
        return {
                "FID": self.FID, 
                "Airline": self.Airline,
                "DepartureLoc": self.DepartureLoc, 
                "ArrivalLoc": self.ArrivalLoc, 
                "Date": self.Date,
                "DepartureTime": str(self.DepartureTime), 
                "Duration": self.Duration, 
                "Price": self.Price
                }
    
    def getPrice(self):
        return {"Price": self.Price}


@app.route("/flight", methods=['GET'])
def get_all_flights():
    flightlist = db.session.scalars(db.select(Flight)).all()
    if len(flightlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "flights": [(flight.json()) for flight in flightlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no flights."
        }
    ), 404

## JSON to pass in  ##
# EXISTS
# {
#     "DepartureLoc": "Singapore",
#     "ArrivalLoc": "Berlin",
#     "DepartureDate": "2024-03-15"
# }

# DON'T EXISTS
# {
#     "DepartureLoc": "Singapore",
#     "ArrivalLoc": "Taipei",
#     "DepartureDate": "2024-03-15"
# }


@app.route("/flight", methods=['POST'])
def searchflights():
    DepartureLoc = request.json.get('DepartureLoc', None)
    ArrivalLoc = request.json.get('ArrivalLoc', None)
    DepartureDate = request.json.get('DepartureDate', None)

    # Convert DepartureDate to a datetime object
    DepartureDate = datetime.strptime(DepartureDate, '%Y-%m-%d')

    flightList = db.session.scalars(db.select(Flight).filter_by(DepartureLoc=DepartureLoc, ArrivalLoc=ArrivalLoc, Date=DepartureDate)).all()
    if len(flightList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "flights": [(flight.json()) for flight in flightList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no flights."
        }
    ), 404

# Get specific flight price by FID
@app.route("/flight/<string:FID>/Price")
def get_price_by_FID(FID):
    flight = db.session.scalars(db.select(Flight).filter_by(FID=FID).limit(1)).first()
    if flight:
        return jsonify(
            {
                "code": 200,
                "data": flight.getPrice()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Price not found."
        }
    ), 404

# Insert new flights (AMQP) Queue: FlightInsert, Routing Key: #.flight
# Receive message
def receiveLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=flight_queue_name, on_message_callback=callback, auto_ack=True)
        print('flights: Consuming from queue:', flight_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"flights: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("flights: Program interrupted by user.")


# Run function based on the message
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nflights: Received an update by " + __file__)
    processInsert(json.loads(body))
    print()


        # self.FID = FID
        # self.Airline = Airline
        # self.DepartureLoc = DepartureLoc
        # self.ArrivalLoc = ArrivalLoc
        # self.Date = Date
        # self.DepartureTime = DepartureTime
        # self.Duration = Duration
        # self.Price = Price

def processInsert(new):
    with app.app_context():
        if not isinstance(new, list):
            return jsonify({
                "code": 400,
                "message": "Expected a list of flight records."
            }), 400

        required_keys = ['FID', 'Airline', 'DepartureLoc', 'ArrivalLoc', 'Date', 'DepartureTime', 'Duration', 'Price']

        for flight_info in new:
            if not all(key in flight_info for key in required_keys):
                return jsonify({
                    "code": 400,
                    "message": "Missing or incorrect keys in a flight record."
                }), 400

            flight = Flight(
                FID=flight_info['FID'],
                Airline=flight_info['Airline'],
                DepartureLoc=flight_info['DepartureLoc'],
                ArrivalLoc=flight_info['ArrivalLoc'],
                Date=flight_info['Date'],
                DepartureTime=flight_info['DepartureTime'],
                Duration=flight_info['Duration'],
                Price=flight_info['Price']
            )

            db.session.add(flight)

        try:
            db.session.commit()
            print("Flights: Recorded the creation in the database")
            return jsonify({"code": 200, "message": "Successfully inserted all flight records."}), 200
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return jsonify({"code": 500, "message": "Internal server error"}), 500



## LAUNCHING FLASK CONNECTION AND AMQP CHANNEL ##

def start_flask():
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        print("Flask thread exiting")

def start_amqp():
    try:
        print("flights: Getting Connection")
        connection = amqp_connection.create_connection()  # get the connection to the broker
        print("flights: Connection established successfully")
        channel = connection.channel()
        receiveLog(channel)
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
