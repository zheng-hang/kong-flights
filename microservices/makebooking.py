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


flight_URL = environ.get('flight_URL') or "http://flight:5000/flight/price/" 
payment_URL = environ.get('payment_URL')


seat_exchangename = environ.get('seat_exchangename') or "seat_topic" # seat exchange name
booking_exchangename = environ.get('booking_exchangename') or "booking_topic" #booking exchange name
notif_exchangename = environ.get('notif_exchangename') or 'notif_topic'
exchangetype="topic" # use a 'topic' exchange to enable interaction

# Instead of hardcoding the values, we can also get them from the environ as shown below
# exchangename = environ.get('exchangename') #order_topic
# exchangetype = environ.get('exchangetype') #topic 

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the seat exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, seat_exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

#if the booking exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, booking_exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status


# JSON RESPONSE FORMAT
# {
#     'email': 'help@gmail.com',
#     'FID': 'SQ 123',
#     'seatcol': 'A',
#     'seatnum': 1
# }

@app.route("/make_booking", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking = request.get_json()
            print("\nReceived a booking request in JSON:", booking)

            # do the actual work
            # 1. Send booking info
            result = processBookingRequest(booking)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processBookingRequest(booking):
    # 2. Get flight price
    # Invoke the flight microservice
    print('\n-----Invoking flight microservice-----')
    price = invoke_http((flight_URL + booking.FID), method='GET')
    print('flight price:', price)


    # 3. reserve seat in Seats
    message = {
                    'fid': booking['fid'],
                    'seatcol': booking['seatcol'],
                    'seatnum': booking['seatnum']
                }

    print('\n\n-----Publishing the (seatupdate) message with routing_key=booking.seat-----')

    channel.basic_publish(exchange=seat_exchangename, routing_key="booking.seat", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nSeat update request published to the RabbitMQ Exchange:", message)


    if price['code'] in range (200,300):
        # 4. Call payment svc
        print('\n-----Call payment service-----')
        payment_result = invoke_http(payment_URL, method='POST', json=price)
        print('payment_result:', payment_result)

    else:
        print('\n-----'+ price['message'] +'-----')


    if payment_result["code"] in range (200,300):
        # 5. Send Notif AMQP
        message = {
                        'email': booking['email'],
                    }

        print('\n\n-----Publishing the (notif) message with routing_key=paymentupdate.notif-----')

        channel.basic_publish(exchange=notif_exchangename, routing_key="paymentupdate.notif", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nNotif request published to the RabbitMQ Exchange:", message)


        # 6. Send booking creation req
        print('\n\n-----Publishing the (booking creation) message with routing_key=paymentupdate.notif-----')

        channel.basic_publish(exchange=notif_exchangename, routing_key="paymentupdate.notif", 
            body=booking, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nBooking creation request published to the RabbitMQ Exchange:", booking)




    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as order fails-----')
    #     print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

    #     # invoke_http(error_URL, method="POST", json=order_result)
    #     channel.basic_publish(exchange=exchangename, routing_key="order.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    #     # make message persistent within the matching queues until it is received by some receiver 
    #     # (the matching queues have to exist and be durable and bound to the exchange)

    #     # - reply from the invocation is not used;
    #     # continue even if this invocation fails        
    #     print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), order_result)

    #     # 7. Return error
    #     return {
    #         "code": 500,
    #         "data": {"order_result": order_result},
    #         "message": "Order creation failure sent for error handling."
    #     }


    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    # else:
    #     # 4. Record new order
    #     # record the activity log anyway
    #     #print('\n\n-----Invoking activity_log microservice-----')
    #     print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')        

    #     # invoke_http(activity_log_URL, method="POST", json=order_result)            
    #     channel.basic_publish(exchange=exchangename, routing_key="order.info", 
    #         body=message)
    
    print("\nOrder published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails
    
    # 5. Send new order to shipping
    # Invoke the shipping record microservice
    print('\n\n-----Invoking shipping_record microservice-----')    
    
    shipping_result = invoke_http(
        shipping_record_URL, method="POST", json=order_result['data'])
    print("shipping_result:", shipping_result, '\n')

    # Check the shipping result;
    # if a failure, send it to the error microservice.
    code = shipping_result["code"]
    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as shipping fails-----')
        print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

        # invoke_http(error_URL, method="POST", json=shipping_result)
        message = json.dumps(shipping_result)
        channel.basic_publish(exchange=exchangename, routing_key="shipping.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
            code), shipping_result)

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "shipping_result": shipping_result
            },
            "message": "Simulated shipping record error sent for error handling."
        }

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "shipping_result": shipping_result
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)