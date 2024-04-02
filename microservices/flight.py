from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ, path
from flask_cors import CORS
from datetime import datetime

flight_queue_name = environ.get('flight_queue_name') or 'FlightInsert'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Flight(db.Model):
    __tablename__ = 'flights'

    FID = db.Column(db.String(10), primary_key=True)
    Airline = db.Column(db.String(255))
    DepartureLoc = db.Column(db.String(255), nullable=False)
    ArrivalLoc = db.Column(db.String(255), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    DepartureTime = db.Column(db.Time, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float(precision=2), nullable=False)
    DepAirportCode = db.Column(db.String(3), nullable=False)
    ArrAirportCode = db.Column(db.String(3), nullable=False)

    def __init__(self, FID, Airline, DepartureLoc, ArrivalLoc, Date, DepartureTime, Duration, Price, DepAirportCode, ArrAirportCode):
        self.FID = FID
        self.Airline = Airline
        self.DepartureLoc = DepartureLoc
        self.ArrivalLoc = ArrivalLoc
        self.Date = Date
        self.DepartureTime = DepartureTime
        self.Duration = Duration
        self.Price = Price
        self.DepAirportCode = DepAirportCode
        self.ArrAirportCode = ArrAirportCode

    def json(self):
        return {
                "FID": self.FID, 
                "Airline": self.Airline,
                "DepartureLoc": self.DepartureLoc, 
                "ArrivalLoc": self.ArrivalLoc, 
                "Date": self.Date,
                "DepartureTime": str(self.DepartureTime), 
                "Duration": self.Duration, 
                "Price": self.Price,
                "DepAirportCode": self.DepAirportCode,
                "ArrAirportCode": self.ArrAirportCode
                }
    
    def getPrice(self):
        return {"Price": self.Price}


with app.app_context():
    # Reflect the tables and print their column names
    meta = db.metadata
    meta.reflect(bind=db.engine)

    for table in meta.sorted_tables:
        print(f"Table: {table.name}")
        for column in table.columns:
            print(f" - {column.name}")


@app.route("/flight")
def get_all_flights():
    flightlist = db.session.scalars(db.select(Flight)).all()
    if len(flightlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "flights": [(flight.json()) for flight in flightlist],
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


@app.route("/flight",  methods=['POST'])
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
@app.route("/flight/price/<string:FID>")
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


@app.route("/insertflights", methods=['POST'])
def insert_flights():
    print(request.json)
    flights = request.json.get('flight')
    print(flights)
    
    required_keys = ['FID', 'Airline', 'DepartureLoc', 'ArrivalLoc', 'Date', 'DepartureTime', 'Duration', 'Price', "DepAirportCode", "ArrAirportCode"]

    if not isinstance(flights, list):
            return jsonify({
                "code": 400,
                "message": "Expected a list of flight records."
            }), 400

    for flight_info in flights:
        print(flight_info)
        print(all(key in flight_info for key in required_keys))
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
            Price=flight_info['Price'],
            DepAirportCode=flight_info['DepAirportCode'],
            ArrAirportCode=flight_info['ArrAirportCode']
        )

        db.session.add(flight)

    try:
        db.session.commit()
        print("Flights: Recorded the creation in the database")
        return jsonify({
                        "code": 200, 
                        "message": "Successfully inserted all flight records.",
                        "data": request.json
                        }), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return jsonify({
                        "code": 500, 
                        "message": "Internal server error"
                        }), 500





## LAUNCHING FLASK CONNECTION AND AMQP CHANNEL ##



if __name__ == "__main__":
    print("This is flask for " + path.basename(__file__) + ": manage flights ...")
    app.run(host='0.0.0.0', port=5000, debug=True)