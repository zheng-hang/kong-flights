from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    # Example function to return a list of users
    # Replace with actual data retrieval and business logic
    users = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Doe"}]
    return jsonify(users)

if __name__ == '__main__':
    app.run(port=5000, debug=True)



# Step 2: Integrate Flask Microservice with the API Gateway
# Ensure your API Gateway (Kong, custom Node.js API Gateway, etc.) is configured to route requests to the Flask microservice. You'll need to add a new route and service in Kong or configure the proxy settings in your custom API Gateway to point to your Flask service's host and port.

# For example, if using Kong:

# Add your Flask microservice as a new service in Kong.
# Configure a route in Kong that forwards to the /users endpoint of your Flask app.