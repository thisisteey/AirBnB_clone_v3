import unittest
from flask import json
from api.v1.app import app

class TestAPIStatus(unittest.TestCase):
    def setUp(self):
        # Set up the flask app for testing
        app.testing = True
        self.app = app.test_client()

    def test_status_endpoint(self):
        # make a Get request to the /status endpoint
        response = self.app.get('/api/v1/status')

        # check if the response status code is 200 ok
        self.assertEqual(response.status_code, 200)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # check if the response JSON contains the expected status
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'OK')

    def test_stats_endpoint(self):
        # make a get request to the /stats endpoint
        response = self.app.get('/api/v1/stats')

        # check if the response status code is 200 ok
        self.assertEqual(response.status_code, 200)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # check if the response JSON contains the expected data
        data = json.loads(response.data)
        self.assertIn('amenities', data)
        self.assertIn('cities', data)
        self.assertIn('places', data)
        self.assertIn('reviews', data)
        self.assertIn('states', data)
        self.assertIn('users', data)

    def test_not_found_endpoint(self):
        # make a get request to unknown endpoint
        response = self.app.get('/api/v1/nop')

        # check if the response code is 400 Not found
        self.assertEqual(response.status_code, 404)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # check if the response JSON contains the expected data
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not  found')
