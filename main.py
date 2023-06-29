import re
import random

from flask import Flask, jsonify, request, abort
from math import radians, sin, cos, sqrt, atan2


# Function to calculate the distance between two points using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Calculate the difference between the latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula to calculate the distance
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance in meters
    distance = earth_radius * c * 1000

    return distance


app = Flask(__name__)

parking_spots = []

for i in range(1, 101):
    latitude = round(random.uniform(12.971, 12.976), 6)
    longitude = round(random.uniform(77.592, 77.599), 6)
    price_per_hour = round(random.uniform(5.0, 20.0), 2)

    parking_spot = {
        'id': i,
        'name': f'Parking Spot {i}',
        'latitude': latitude,
        'longitude': longitude,
        'price_per_hour': price_per_hour
    }

    parking_spots.append(parking_spot)


# Global list to store reservations
reservations = []


@app.route('/signup', methods=['POST'])
def signup():
    # Access the user's phone number/email from the request data
    phone_number = request.json.get('phone_number')
    email = request.json.get('email')

    # Validate phone number format
    phone_regex = r'^\d+$'  # Customize the regex pattern according to your requirements
    if not re.match(phone_regex, phone_number):
        abort(400, 'Invalid phone number')

    # Validate email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Customize the regex pattern according to your requirements
    if not re.match(email_regex, email):
        abort(400, 'Invalid email address')

    # Implement your signup logic here (e.g., store the user's information in a database)
    # Return a success message or appropriate response
    return jsonify({'message': 'Signup successful'})


@app.route('/parking_spots', methods=['GET'])
def get_parking_spots():
    # Return all parking spots
    return jsonify(parking_spots)


@app.route('/parking_spots/nearby', methods=['GET'])
def get_nearby_parking_spots():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('long'))
    radius = float(request.args.get('radius'))

    nearby_spots = []
    for spot in parking_spots:
        spot_latitude = spot['latitude']
        spot_longitude = spot['longitude']
        distance = calculate_distance(latitude, longitude, spot_latitude, spot_longitude)
        if distance <= radius:
            nearby_spots.append(spot)

    return jsonify(nearby_spots)


from datetime import datetime


# ...

@app.route('/parking_spots/<int:spot_id>/reserve', methods=['POST'])
def reserve_parking_spot(spot_id):
    # Access the reservation data from the request
    data = request.get_json()
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')

    # Convert the start_time and end_time strings to datetime objects
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

    # Check if someone has already booked the same spot at the same time
    for reservation in reservations:
        if reservation['spot_id'] == spot_id:
            existing_start_time = datetime.strptime(reservation['start_time'], '%Y-%m-%d %H:%M:%S')
            existing_end_time = datetime.strptime(reservation['end_time'], '%Y-%m-%d %H:%M:%S')

            if start_time <= existing_end_time and end_time >= existing_start_time:
                abort(400, 'This parking spot is already booked at the specified time')

    # Create a new reservation entry
    new_reservation = {
        'spot_id': spot_id,
        'start_time': start_time_str,
        'end_time': end_time_str
    }
    reservations.append(new_reservation)

    # Return a success message or appropriate response
    return jsonify({'message': 'Parking spot reserved successfully'})


@app.route('/reservations', methods=['GET'])
def get_reservations():
    # Implement logic to retrieve reservations for the current user (if applicable)
    # For now, let's return all reservations in the global list
    return jsonify(reservations), 200


if __name__ == '__main__':
    app.run(debug=True)
