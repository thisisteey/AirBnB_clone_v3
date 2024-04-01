"""
unittests to handle the tasks described for the City API endpoints:
"""
import unittest
from flask import json
from api.v1.app import app


class TestAPICityStatus(unittest.TestCase):
    """unittest case for api endpoint """
    def setUp(self):
        """Set up the flask app for testing"""
        app.testing = True
        self.app = app.test_client()

    def test_get_cities_by_state_id(self):
        """
        a GET request to retrieve all City objects of
        a State by state_id
        """
        # create a post request to retrieve id"
        data = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        # retrieve all City objects of a State by state_id
        response = self.app.get('/api/v1/states/{}/cities'.format(state_id))

        # check if the response status code is 200 OK or 404 Not found
        self.assertIn(response.status_code, [200, 404])

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        if response.status_code == 200:
            # check the response data structure and content
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))


    def test_create_city(self):
        """
        POST request to create a City object under a State by state_id
        """
        # create a post request to retrieve id"
        data_0 = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data = {'name': 'San Francisco'}
        response = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data),
                                 content_type='application/json')
        
        # check if the response status code is 201 Created
        if response.status_code == 201:
            # check the response data structure and content
            created_city = json.loads(response.data)
            self.assertIn('__class__', created_city)
            self.assertIn('state_id', created_city)
            self.assertIn('created_at', created_city)
            self.assertIn('id', created_city)
            self.assertIn('name', created_city)
            self.assertIn('updated_at', created_city)
        elif response.status_code == 400:
            # check error message or content
            error_data = json.loads(response.data)
            self.assertIn('message', error_data)

        # clean up
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))       

    def test_update_city(self):
        """
        PUT request to update a City object by city_id
        """
        # create a post request to retrieve id"
        data_0 = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data_1 = {'name': 'San Francisco'}
        response_1 = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created city
        city_id = json.loads(response_1.data)['id']
        data = {'name': 'Los Angeles'}

        response = self.app.put('/app/v1/cities/{}'
                                .format(city_id),
                                data=json.dumps(data),
                                content_type='application/json')

        if response.status_code == 200:
            # Check the response data structure and content for the updated City object
            updated_city = json.loads(response.data)
            self.assertIn('__class__', updated_city)
            self.assertIn('created_at', updated_city)
            self.assertIn('id', updated_city)
            self.assertIn('name', updated_city)
            self.assertIn('state_id', updated_city)
            self.assertIn('updated_at', updated_city)
        elif response.status_code == 404:
            # check the error message or content for a 404 response
            error_data = json.loads(response.data)
            self.assertIn('error', error_data)

        # clean up
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))

    def test_get_city_by_id(self):
        # create a post request to retrieve id"
        data_0 = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data_1 = {'name': 'San Francisco'}
        response_1 = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created city
        city_id = json.loads(response_1.data)['id']
        response = self.app.get('/api/v1/cities/{}'.format(city_id))

        # Check if the response status code is 200 OK or 404 Not Found
        self.assertIn(response.status_code, [200, 404])

        # Check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        if response.status_code == 200:
            # Check the response data structure and content for a valid City object
            city_data = json.loads(response.data)
            self.assertIn('__class__', city_data)
            self.assertIn('created_at', city_data)
            self.assertIn('id', city_data)
            self.assertIn('name', city_data)
            self.assertIn('state_id', city_data)
            self.assertIn('updated_at', city_data)
        elif response.status_code == 404:
            # check the error message or content for a 404 response
            error_data = json.loads(response.data)
            self.assertIn('error', error_data)

        # clean up
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))

    def test_delete_city(self):
        """test make a delete request to the /cities/<city_id>"""
        # create a post request to retrieve id"
        data_0 = {'name': 'Califonrnia'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data_1 = {'name': 'San Francisco'}
        response_1 = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created city
        city_id = json.loads(response_1.data)['id']
        # make a DELETE request tot the /states/<state_id> endpoint
        response = self.app.delete('/api/v1/cities/{}'.format(city_id))
        # check if the response status code is correct
        self.assertEqual(response.status_code, 200) 
        # check if the response content type is JSON
        self.assertEqual('application/json', response.content_type)
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))

    def test_delete_city_not_valid(self):
        """test make a delete request to the /cities/<city_id>
        where city id is invalid
        """
        # Get id of created city
        city_id = 'Play'
        # make a DELETE request tot the /states/<state_id> endpoint
        response = self.app.delete('/api/v1/cities/{}'.format(city_id))
        # check if the response status code is correct
        self.assertEqual(response.status_code, 200) 
        # check if the response content type is JSON
        self.assertEqual('application/json', response.content_type)
        # check if the response JSON contains the expected data
        data = json.loads(response.data)
        self.assertEqual(data['error'], {})
    
    def test_create_invalid_city(self):
        """
        POST request to create a City object under a State by state_id
        where state_id is invalid
        """
        state_id = 'CheckTruth'
        data = {'name': 'San Francisco'}
        response = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data),
                                 content_type='application/json')
        
        # check if the response status code is 404 error
        self.assertEqual(response.status_code, 404)

    def test_invalid_json(self):
        """
        Test if the HTTP body post request is not a valid JSON,
        raise a 400 error with the message Not a JSON
        """
        # create a post request to retrieve id"
        data_0 = {'name': 'Nigeria'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data = 'San Francisco'
        response = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=data)
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Not a JSON')
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))

    def test_missing_name(self):
        """
        Test if the HTTP body post request is not a valid JSON,
        raise a 400 error with the message Not a JSON
        """
        # create a post request to retrieve id"
        data_0 = {'name': 'Nigeria'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data = {'namee': 'San Francisco'}
        response = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Missing name')
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))
      
    def test_put_invalid_json(self):
        """
        Test if the HTTP body put request is not a valid JSON,
        raise a 400 error with the message Not a JSON
        """
        # create a post request to retrieve id"
        data_0 = {'name': 'Lagos'}
        response_0 = self.app.post('/api/v1/states', json=data_0)
        # Get id of the created state
        state_id = json.loads(response_0.data)['id']
        data_1 = {'name': 'Ikeja'}
        response_1 = self.app.post('/api/v1/states/{}/cities'
                                 .format(state_id),
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created city
        city_id = json.loads(response_1.data)['id']
        data = 'Los Angeles'

        response = self.app.put('/app/v1/cities/{}'
                                .format(city_id),
                                data=data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Not a JSON')
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(state_id))
