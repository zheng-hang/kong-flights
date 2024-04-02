from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)


seatReserve_URL = environ.get("seat_URL") or "http://localhost:5000/reserveseat"
seatUpdate_URL = environ.get("seat_URL") or "http://localhost:5000/updateseat"
passengerbooking_URL = environ.get("passengerbooking_URL") or "http://localhost:5000/update"
# payment_url =
# notification_url = environ.get("notification_URL") 



# exchangename_booking = "booking_topic"
# exchangename_seat_change =  "seat_change_topic"
exchangename_notification = "Notif"
# exchangename_payment = "" not done

exchangetype="topic"

#create a connection and a channel to the broker to publish messages to seat_, passengerbookigns, notifications and 
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program ()
if not amqp_connection.check_exchange(channel, exchangename_notification, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

# if not amqp_connection.check_exchange(channel, exchangename_booking, exchangetype):
#     print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
#     sys.exit(0)  # Exit with a success status



@app.route("/seatchange", methods=['POST'])
def seat_change():
    if request.is_json:
        try:
            data = request.get_json()
            print("\nReceived a seat change request with:", data)
            
            result = processSeatChange(data)
            print('\n------------------------')
            print('\nresult: ', result)

            #SCENARIO 8: Return change confirmation to UI -- CHECK ray
            return jsonify(result)
        
        except Exception as e:
            return jsonify({
                "code": 400,
                "message": str(e)
            })



def processSeatChange(seat):
    # send the seat change into seat
    # invoke seat microservice

    print("invoking seat microservice")

    # SCENARIO 2: reserving the seat 
    # data: the JSON input when needed by the http method;
    # create a copy of the seat dictionary
    seat_copy = seat.copy()

    # remove 'bid' from the copy
    seat_copy.pop('bid', None)
    reserve_seat = invoke_http(seatReserve_URL, method='PUT', json=seat_copy)
    print("Seat reserved" + reserve_seat)

    code_reserve_seat = reserve_seat['code']
    if code_reserve_seat not in range(200, 300):
        return {
            "code": 500,
            "data": "Seat reservation failed"
        }
    else:

        # UNCOMMENT ONCE PAYMENT IS DONE
        #SCENARIO 3-7: send payment requests to payment system (NOT DONE)
        #
        # price_result = invoke_http(payment_url, method='POST', json=seat)
        # print("Payment request sent to payment system")
        # if price_result['code'] not in range(200, 300):
        #     this SCENARIO will trigger if any of the above steps have failed but if SCENARIO 2 is successful
        #     SCENARIO 7: If fail, updating old seat availability
        #     fail_update = invoke_http(seatUpdate_URL, method='PUT', json=seat_copy)
        #     print("Seat reserved" + fail_update)
        #     return {
        #         "code": 500,
        #         "data": "Payment failed"
        #     }

              


        #SCENARIO 9: send to notification (NOT DONE) AMQP
        channel.basic_publish(exchange=exchangename_notification, routing_key="do.notif", 
            body=json.dumps(seat), properties=pika.BasicProperties(delivery_mode = 2))
        
        print("\n Notification to the RabbitMQ Exchange:", seat)


        #SCENARIO 10: update passenger bookings
        # this case is seat change so bid in message 

        # create a copy of the seat dictionary
        seat_copy2 = seat.copy()

        # remove 'bid' from the copy
        seat_copy2.pop('fid', None)

        update_flight_booking = invoke_http(passengerbooking_URL, method='PUT', json=seat_copy2)
        print("Seat reserved" + update_flight_booking)

        if update_flight_booking['code'] not in range(200, 300):
            return {
                "code": 500,
                "data": "Flight booking update failed"
            }

        #SCENARIO 12: Update old flight seat to available
        # first get the fid,seatcol and seatnum of the old seat
        person_pid = seat['bid']
        original_seat = get_original_booking(person_pid)
        original_seat.pop('bid', None)

        update_old_seat = invoke_http(seatUpdate_URL, method='PUT', json=original_seat)
        print("Seat reserved" + update_old_seat) ## HTTP function for updating the old seat, scenario #

        if update_old_seat['code'] not in range(200, 300):
            return {
                "code": 500,
                "data": "Old seat update failed"
            }
        print("\nSeat update request published to the RabbitMQ Exchange:")

        print('\n\n-----Publishing the (bookingcreation) message with routing_key=createbooking.booking-----')

        # UNCOMMENT ONCE EVERYTHING IS DONE
        #SCENARIO 8: returning the output to the UI
        # return {
        #     "payment_details" : price_result,
        #     "seat" : seat,
        # }

# for retrieving the person's original bid
def get_original_booking(person_bid):
    response = requests.get(f"http://localhost:5000/booking/{person_bid}")
    data = response.json()
    if data['code'] == 200 and data['data']:
        return data['data'][0]
    return None
 



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5103, debug=True)