import json
import unittest
from main import app, reservations


class ParkingAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_signup_valid_input(self):
        payload = {
            'phone_number': '1234567890',
            'email': 'user@example.com'
        }
        response = self.app.post('/signup', data=json.dumps(payload),
                                 content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Signup successful')

    def test_signup_invalid_phone_number(self):
        payload = {
            'phone_number': 'ABCD',  # Invalid phone number format
            'email': 'user@example.com'
        }
        response = self.app.post('/signup', data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid phone number', response.get_data(as_text=True))

    def test_signup_invalid_email(self):
        payload = {
            'phone_number': '1234567890',
            'email': 'userexample'  # Invalid email format
        }
        response = self.app.post('/signup', data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid email address', response.data)

    def test_get_parking_spots(self):
        response = self.app.get('/parking_spots')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_nearby_parking_spots(self):
        query_string = {
            'lat': 12.9715987,
            'long': 77.5945627,
            'radius': 1000
        }
        response = self.app.get('/parking_spots/nearby', query_string=query_string)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_reserve_parking_spot_successful(self):
        # Add a dummy reservation to simulate an existing booking
        existing_reservation = {
            'spot_id': 1,
            'start_time': '2023-06-30 10:00:00',
            'end_time': '2023-06-30 12:00:00'
        }
        reservations.append(existing_reservation)

        # Make a reservation request for a different time slot
        data = {
            'start_time': '2023-06-30 14:00:00',
            'end_time': '2023-06-30 16:00:00'
        }
        response = self.app.post('/parking_spots/1/reserve', data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data),
                         {'message': 'Parking spot reserved successfully'})

    def test_reserve_parking_spot_conflict(self):
        # Add a dummy reservation to simulate an existing booking
        existing_reservation = {
            'spot_id': 1,
            'start_time': '2023-06-30 10:00:00',
            'end_time': '2023-06-30 12:00:00'
        }
        reservations.append(existing_reservation)

        # Make a reservation request for the same time slot
        data = {
            'start_time': '2023-06-30 11:00:00',
            'end_time': '2023-06-30 13:00:00'
        }
        response = self.app.post('/parking_spots/1/reserve', data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This parking spot is already booked at the specified time', response.data)

    def tearDown(self):
        # Reset the reservations list after each test case
        reservations.clear()

    def test_get_reservations(self):
        response = self.app.get('/reservations')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()
