import unittest
from flask import json
from api.v1.app import app


class TestAPIStatus(unittest.TestCase):
    """unittest case for api endpoint """
    def setUp(self):
        """Set up the flask app for testing"""
        app.testing = True
        self.app = app.test_client()

    def test_status_endpoint(self):
        """ make a Get request to the /status endpoint """
        response = self.app.get('/api/v1/status')

        # check if the response status code is 200 ok
        self.assertEqual(response.status_code, 200)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # check if the response JSON contains the expected status
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'OK')

    def test_stats_endpoint(self):
        """make a get request to the /stats endpoint"""
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
        """make a get request to unknown endpoint"""
        response = self.app.get('/api/v1/nop')

        # check if the response code is 400 Not found
        self.assertEqual(response.status_code, 404)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # check if the response JSON contains the expected data
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not found')

    def test_get_states(self):
        """make a get request ti the /states endpoint"""
        response = self.app.get('/api/v1/states')

        # check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

    def test_post_state(self):
        """
        test make a post request to the /states endpoint with
        valid JSON data
        """
        data = {'name': 'Califonrnia'}
        response = self.app.post('/api/v1/states', json=data)

        # check if the response status code is 201 CREATED
        self.assertEqual(response.status_code, 201)

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # delete the created state
        state_id = json.loads(response.data)['id']
        self.app.delete('/api/v1/states/{}'.format(state_id))

    def test_get_state_by_id(self):
        """test get request to retrieve a state by state_id"""
        # create a post request to retrieve id"
        data = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        # make a GET request to retrieve a state by state_id
        response = self.app.get('/api/v1/states/{}'.format(state_id))

        # check if the response code is 200
        self.assertIn('application/json', response.content_type)
        if response.status_code == 200:
            # Check the response data structure and content
            data = json.loads(response.data)
            self.assertIn('__class__', data)
            self.assertIn('created_at', data)
            self.assertIn('id', data)
            self.assertIn('name', data)
            self.assertIn('updated_at', data)
        elif response.status_code == 404:
            # Optionally, check the error message or content for a 404 response
            error_data = json.loads(response.data)
            self.assertIn('error', error_data)

        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))

    def test_delete_state(self):
        """test make a delete request to the /states/"""
        # create a post request to test delete endpoint
        data = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        # make a DELETE request tot the /states/<state_id> endpoint
        response = self.app.delete('/api/v1/states/{}'.format(state_id))

        # check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # check if the response content type is JSON
        self.assertEqual('application/json', response.content_type)

    def test_put_state(self):
        """ Test Put request"""
        # create a post request to test delete endpoint
        data = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        # Make a PUT request to the /states/<state_id>
        data = {'name': 'California is so cool'}
        response = self.app.put('/api/v1/states/{}'
                                .format(state_id), json=data)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))
