from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from datetime import datetime

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

# Insert new flights (AMQP)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
