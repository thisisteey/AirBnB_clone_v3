"""
unittests to handle the tasks described for the City API endpoints:
"""
import unittest
from flask import json
from api.v1.app import app


class TestAPIAmenityStatus(unittest.TestCase):
    """unittest case for api Amenity endpoint """
    def setUp(self):
        """Set up the flask app for testing"""
        app.testing = True
        self.app = app.test_client()

    def test_get_amenities(self):
        """Send a GET request to retrieve all amenities"""
        response = self.app.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        # Assert the structure of the response JSON
        self.assertIn('amenities', response.json)
        self.assertIsInstance(response.json['amenities'], list)

    def test_get_amenity(self):
        """
        Send a GET request to retrieve a specific amenity
        amenity_id> with a valid ID
        """
        data0 = {'name': 'Test Amenity'}
        response0 = self.app.post('/api/v1/amenities', json.dumps(data0))
        amenity_data = json.loads(response0.data)
        amenity_id = amenity_data['id']
        response = self.app.get('/api/v1/amenities/{}'.format(amenity_id))
        # check if the response status code is 200 OK or 404 Not found
        self.assertIn(response.status_code, [200, 404])

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        if response.status_code == 200:
            # check the response data structure and content
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

        # delete the created amenity
        self.app.delete('/api/v1/amenities/{}'.format(amenity_id))

    def test_get_amenity_invalid(self):
        """
        Send a GET request to retrieve a specific amenity
        amenity_id> with a invalid ID)
        """
        response = self.app.get('/api/v1/amenities/<amenity_id>')
        # Assert that the status code is 404 for a non-existent amenity
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        """ Send a DELETE request to delete an existing amenity
        with a valid ID
        """
        data0 = {'name': 'Test Amenity'}
        response0 = self.app.post('/api/v1/amenities', json.dumps(data0))
        amenity_data = json.loads(response0.data)
        amenity_id = amenity_data['id']
        response = self.app.delete('/api/v1/amenities/{}'.format(amenity_id))
        # Assert that the status code is 404 for a non-existent amenity
        self.assertEqual(response.status_code, 200)

    def test_create_amenity(self):
        """Send a POST request to create a new amenity"""
        data = {'name': 'Test Amenity'}
        response = self.app.post('/api/v1/amenities', json.dumps(data))
        self.assertEqual(response.status_code, 201)
        # Assert the structure of the response JSON
        amenity_data = json.loads(response.data)
        self.assertIn('name', amenity_data)
        self.assertEqual(amenity_data['name'], 'Test Amenity')
        # clean up
        self.app.delete('/api/v1/amenities/{}'.format(amenity_data['id']))

    def test_update_amenity(self):
        """Send a PUT request to update an existing amenity
        with a valid ID
        """
        data0 = {'name': 'Test Amenity'}
        response0 = self.app.post('/api/v1/amenities', json.dumps(data0))
        amenity_data = json.loads(response0.data)
        amenity_id = amenity_data['id'] 
        data = {'name': 'Updated Amenity'}
        response = self.app.put('/api/v1/amenities/{}'.format(amenity_id),
                                data=json.dumps(data))
        # Assert that the status code is 404 for a non-existent amenity
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_invalid(self):
        """Send a PUT request to update an existing amenity
        with a invalid json
        """
        data0 = {'name': 'Test Amenity'}
        response0 = self.app.post('/api/v1/amenities', json.dumps(data0))
        amenity_data = json.loads(response0.data)
        amenity_id = amenity_data['id'] 
        data = 'Updated Amenity'
        response = self.app.put('/api/v1/amenities/{}'.format(amenity_id),
                                data=json.dumps(data))
        # Assert that the status code is 404 for a invalid amenity
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Not a JSON')
        # delete the created state
        self.app.delete('/api/v1/amenities/{}'.format(amenity_id))
