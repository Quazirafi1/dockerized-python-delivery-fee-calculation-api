from flask import Flask, request, jsonify
from datetime import datetime
import math

# fixed base fare for delivery 
base_fare = 2
date_format = "%Y-%m-%dT%H:%M:%SZ"

app = Flask(__name__)

# request body validation 
def validate_request(data):
    required_fields = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
    
    # missing fields checking
    if not all(field in data for field in required_fields):
        return False, "Missing required fields"

    # validation of data types
    if not (isinstance(data['cart_value'], int) and isinstance(data['delivery_distance'], int) and isinstance(data['number_of_items'], int) and isinstance(data['time'], str)):
        return False, 'Invalid data types'
    
    # validation of date-time format 
    try:
        datetime.strptime(data['time'], date_format)
    except ValueError:
        return False, 'Invalid date-time format'
    
    return True, 'Valid request'

# surcharge calculation for cart value less than 10€
def calculate_surcharge_for_small_order(cart_value):
    return 10 - cart_value

# surcharge calculation for distances over 1000m, 1€ is added for every additional 500 meters
def calculate_surcharge_for_longer_distance(delivery_distance):
    return base_fare + math.ceil(((delivery_distance-1000)/500))

# surcharge calculation for additional items; every additional items above 4 items results in a surcharge of 0.50€
# however, number of items more than 12 results in an extra bulk fee of 1.20€
def calculate_surcharge_for_additional_items(number_of_items):
    if number_of_items <= 12:
        return (number_of_items-4)*0.50
    else:
        return (number_of_items-4)*0.50 + 1.20 

# determination of delivery fee based on cart value
def calculate_delivery_fee_based_on_cart_value(cart_value):
    if cart_value<10:
        return calculate_surcharge_for_small_order(cart_value)
    return 0

# determination of delivery fee based on delivery distance
def calculate_delivery_fee_based_on_distance(delivery_distance):
    if delivery_distance > 1000:
        return calculate_surcharge_for_longer_distance (delivery_distance)
    return base_fare

# determination of delivery fee based on number of items
def calculate_delivery_fee_based_on_items(number_of_items):
    if number_of_items > 4:
        return calculate_surcharge_for_additional_items(number_of_items)
    return 0

# check if the delivery time falls within the rush hour period
def if_rush_hour(time):
    date_obj = datetime.strptime(time, date_format)
    # rush hour is defined as Friday between 15:00 and 19:00
    # Monday corresponds to 0 in the weekday() of the datetime object and Sunday corresponds to 6 
    # so Friday corresponds to 4  
    if date_obj.weekday() == 4 and date_obj.hour >= 15 and date_obj.hour <= 19:
        return True

#api 
@app.route("/calculate-delivery-fee", methods = ["POST"])
def calculate_delivery_fee():
    #parse JSON data from request body
    data = request.get_json()

    is_valid_request, validation_msg_body = validate_request(data)

    if not is_valid_request:
        return jsonify({'error': validation_msg_body}), 400

    cart_value = data.get('cart_value')/100 # converting cents to €
    delivery_distance = data.get('delivery_distance')
    number_of_items = data.get('number_of_items')
    time = data.get('time')
    
    delivery_fee = 0
    
    # delivery fee calculation based on cart value, distance, and number of items
    delivery_fee = delivery_fee + calculate_delivery_fee_based_on_cart_value(cart_value)
    delivery_fee = delivery_fee + calculate_delivery_fee_based_on_distance(delivery_distance)
    delivery_fee = delivery_fee + calculate_delivery_fee_based_on_items(number_of_items)

    # free delivery for orders above or equal to 200€
    if cart_value >= 200:
        delivery_fee = 0
    test = False

    # application of rush hour rates
    if if_rush_hour(time):
        delivery_fee = delivery_fee * 1.2

    # maximum delivery fee is 15€
    if delivery_fee > 15:
        delivery_fee = 15

    return_data = {
        "delivery_fee": delivery_fee
    }
    return jsonify(return_data), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)