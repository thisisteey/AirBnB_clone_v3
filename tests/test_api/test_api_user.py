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

    def test_get_user_by_id(self):
        """
        a GET request to retrieve all user objects of
        a User by user_id
        """
        # create a post request to retrieve id"
        data = {'name': 'Person'}
        response_0 = self.app.post('/api/v1/users', json=data)
        # Get id of the created state
        user_id = json.loads(response_0.data)['id']
        # retrieve all City objects of a State by state_id
        response = self.app.get('/api/v1/users/{}'.format(user_id))

        # check if the response status code is 200 OK or 404 Not found
        self.assertIn(response.status_code, [200, 404])

        # check if the response content type is JSON
        self.assertIn('application/json', response.content_type)

        if response.status_code == 200:
            # check the response data structure and content
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

        # delete the created state
        self.app.delete('/api/v1/users/{}'.format(user_id))


    def test_create_user(self):
        """
        POST request to create a user
        """
        # create a post request to retrieve id"
        data = {'name': 'Francisco',
                'email': 'love@email.com',
                'password': 'three'
                }
        response = self.app.post('/api/v1/users',
                                 data=json.dumps(data),
                                 content_type='application/json')

        # check if the response status code is 201 Created
        self.assertEqual(response.status_code, 201)
        created_user = json.loads(response.data)
        self.app.delete('/api/v1/users/{}'.format(created_user['id']))

    def test_update_user(self):
        """
        PUT request to update a User object by user_id
        """
        # create a post request to retrieve id"
        data_1 = {'name': 'Francisco',
                'email': 'love@email.com',
                'password': 'three'}
        response_1 = self.app.post('/api/v1/users/',
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created user
        user_id = json.loads(response_1.data)['id']
        data = {'name': 'Angeles'}

        response = self.app.put('/app/v1/users/{}'
                                .format(user_id),
                                data=json.dumps(data),
                                content_type='application/json')

        self.assertEqual(response.status_code, 200)
        # clean up
        # delete the created user
        self.app.delete('/api/v1/states/{}'.format(user_id))

    def test_get_user_by_id(self):
        """Retrieves a User object: GET /api/v1/users/<user_id>"""
        # create a post request to retrieve id"
        data_1 = {'name': 'Francisco',
                'email': 'love@email.com',
                'password': 'three'}
        response_1 = self.app.post('/api/v1/users/',
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created user
        user_id = json.loads(response_1.data)['id']
        response = self.app.get('/api/v1/users/{}'.format(user_id))
        self.assertEqual(response.status_code, 200)
        # clean up
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(user_id))

    def test_get_user_by_invalid_id(self):
        """Retrieves a User object: GET /api/v1/users/<user_id>"""
        # Get invalid id of created user
        user_id = 'invalidID'
        response = self.app.get('/api/v1/users/{}'.format(user_id))
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        """test make a delete request to the /users/<user_id>"""
        # create a post request to retrieve id"
        data_1 = {'name': 'Francisco',
                'email': 'love@email.com',
                'password': 'three'}
        response_1 = self.app.post('/api/v1/users/',
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created city
        user_id = json.loads(response_1.data)['id']
        # make a DELETE request tot the /states/<state_id> endpoint
        response = self.app.delete('/api/v1/users/{}'.format(user_id))
        # check if the response status code is correct
        self.assertEqual(response.status_code, 200) 
        # check if the response content type is JSON
        data = json.loads(response.data)
        self.assertEqual(data['error'], {})
        # delete the created state
        self.app.delete('/api/v1/states/{}'.format(user_id))

    def test_delete_user_not_valid(self):
        """test make a delete request to the /users/<user_id>
        where user id is invalid
        """
        # Get id of created city
        user_id = 'testId'
        # make a DELETE request tot the /states/<state_id> endpoint
        response = self.app.delete('/api/v1/users/{}'.format(user_id))
        # check if the response status code is correct
        self.assertEqual(response.status_code, 404) 

    
    def test_create_invalid_user(self):
        """
        POST request to create a User object by user_id
        where user_id is invalid
        """
        user_id = 'CheckTruth'
        data = {'name': 'Francisco',
                'email': 'love@email.com',
                'password': 'three'}
        response = self.app.post('/api/v1/users/{}'
                                 .format(user_id),
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
       # create a post request to retrieve id"
        data_1 = {'name': 'Francisco',
                'email': 'love@email.com',
                'password': 'three'}
        response_1 = self.app.post('/api/v1/users/',
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created user
        user_id = json.loads(response_1.data)['id']
    
        data = 'San Francisco'
        response = self.app.post('/api/v1/users/{}'
                                 .format(user_id),
                                 data=data)
        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Not a JSON')
        # delete the created user
        self.app.delete('/api/v1/users/{}'.format(user_id))

    def test_missing_email(self):
        """
        Test if the HTTP body post request is not a valid JSON,
        raise a 400 error with the message Not a JSON
        """
        # create a post request to retrieve id"
        data_1 = {'name': 'Francisco',
                'email': 'love@mail.com',
                'password': 'three'}
        response_1 = self.app.post('/api/v1/users/',
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created user
        user_id = json.loads(response_1.data)['id']
        # create a post request to retrieve id"
        data = {'name': 'Francisco',
                'password': 'three'}
        response = self.app.post('/api/v1/users/{}'
                                 .format(user_id),
                                 data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Missing email')
        # delete the created state
        self.app.delete('/api/v1/users/{}'.format(user_id))

    def test_missing_password(self):
        """
        Test if the HTTP body post request is not a valid JSON,
        raise a 400 error with the message Not a JSON
        """
        # create a post request to retrieve id"
        data_1 = {'name': 'Francisco',
                'email': 'love@mail.com',
                'password': 'three'}
        response_1 = self.app.post('/api/v1/users/',
                                 data=json.dumps(data_1),
                                 content_type='application/json')
        # Get id of created user
        user_id = json.loads(response_1.data)['id']
        # create a post request to retrieve id"
        data = {'name': 'Francisco',
                'email': 'love@mail.com'}
        response = self.app.post('/api/v1/users/{}'
                                 .format(user_id),
                                 data=json.dumps(data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        error_data = json.loads(response.data)
        self.assertEqual(error_data['error'], 'Missing password')
        # delete the created state
        self.app.delete('/api/v1/users/{}'.format(user_id)) 

