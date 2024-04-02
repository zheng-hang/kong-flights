# # import flask
# # import stripe
# from flask import Flask, request

# app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# def webhook():

#     return True

# @app.route('/endpoint', methods=['GET']) #call from complex service
# def endpoint():
#     return True

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)


# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import json
import os
import stripe

from flask import Flask, jsonify, request

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_51P18AIAnvyvXxSjmUXQ1t7oatLheiqCb5ww9HDOMbLjYBdZMU7EheWShhlpoD4OM68E4hFzfB8XubkjpAKecYtGp00FTxgnyoG"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_sktXeIKjyXf3zaEDcy3aOEsxhLt8s0PB'

app = Flask(__name__)

@app.route('/endpoint', methods=['POST']) #call from complex service
def endpoint():
    price = request.get_json()["price"]
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'unit_amount': price, #pass in from complex service, represents in cents
            'product_data': {
                'name': 'Tickets',
            },
        },
        'quantity': 1,
    }],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
)
    
    checkout_url = session.url
    print(checkout_url)


    return jsonify(checkout_url=checkout_url)
    


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     event = None
#     payload = request.get_data(as_text=True)
#     sig_header = request.headers.get('Stripe-Signature')

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
        
#     except ValueError as e:
#         # Invalid payload
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         raise e
    
#     if event['type'] != 'checkout.session.completed':
#         return jsonify(success=False)
#     # Handle the event
#     # if event['type'] == 'checkout.session.completed':
#     #   session = event['data']['object']
#     # # 
#     # else:
#     #   print('Unhandled event type {}'.format(event['type']))

#     email = event['data']['object']['customer_email']
#     return jsonify(email=email)


@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400

    if event['type'] != 'checkout.session.completed':
        return jsonify({'status': 'failed'}), 400

    session = event['data']['object']
    customer_email = session['customer_details']['email']
    return jsonify({'email': customer_email}), 200

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True)