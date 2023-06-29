# Car Parking Project

This project provides a Flask API for managing car parking spots and reservations.

## Prerequisites

- Python 3.7 or above
- Flask

## Setup and Usage

1. Create a Python virtual environment:


2. Activate the virtual environment:

- For macOS/Linux:

  ```
  source venv/bin/activate
  ```

- For Windows:

  ```
  venv\Scripts\activate
  ```

3. Install the required dependencies:


4. Run the Flask application:

- For macOS/Linux:

  ```
  python3 main.py
  ```

- For Windows:

  ```
  python main.py
  ```

The application should now be running at `http://localhost:5000`.

## Running Tests

To run the test cases, use the following command:


## API Endpoints

- `POST /signup`: Sign up using phone number and email.

Sample cURL: 

    curl -X POST -H "Content-Type: application/json" -d '{"phone_number": "+1234567890", "email": "user@example.com"}' http://localhost:5000/signup


- `GET /parking_spots`: Get all available parking spots.

Sample cURL:

    curl http://localhost:5000/parking_spots

- `POST /parking_spots/<spot_id>/reserve`: Reserve a parking spot.

Sample cURL:

    curl -X POST -H "Content-Type: application/json" -d '{"start_time": "2023-06-30 10:00:00", "end_time": "2023-06-30 12:00:00"}' http://localhost:5000/parking_spots/1/reserve


- `GET /reservations`: Get existing reservations.

Sample cURL:

    curl http://localhost:5000/reservations


Please refer to the API documentation for detailed information about each endpoint.
