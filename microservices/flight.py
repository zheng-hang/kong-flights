from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Flight(db.Model):
    __tablename__ = 'Flight'

    FID = db.Column(db.String(6), primary_key=True)
    DepartureLoc = db.Column(db.String(255), nullable=False)
    ArrivalLoc = db.Column(db.String(255), nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
    DepartureTime = db.Column(db.DateTime, nullable=False)
    Duration = db.Column(db.Int, nullable=False)
    Price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, FID, DepartureLoc, ArrivalLoc, Date, DepartureTime, Duration, Price):
        self.FID = FID
        self.DepartureLoc = DepartureLoc
        self.ArrivalLoc = ArrivalLoc
        self.Date = Date
        self.DepartureTime = DepartureTime
        self.Duration = Duration
        self.Price = Price

    def json(self):
        return {"FID": self.FID, "DepartureLoc": self.DepartureLoc, "ArrivalLoc": self.ArrivalLoc, "Date": self.Date,
                "DepartureTime": self.DepartureTime, "Duration": self.Duration, "Price": self.Price}
    
    def getPrice(self):
        return {"Price": self.Price}

# Get all flights
@app.route("/flight")
def get_all():
    flightList = db.session.scalars(db.select(Flight)).all()
    if len(flightList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "flights": [flight.json() for flight in flightList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no flights."
        }
    ), 404


# Search by Flight ID
@app.route("/flight/<string:FID>")
def find_by_FID(FID):
    flight = db.session.scalars(db.select(Flight).filter_by(FID=FID).limit(1)).first()
    if flight:
        return jsonify(
            {
                "code": 200,
                "data": flight.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Flight not found."
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
