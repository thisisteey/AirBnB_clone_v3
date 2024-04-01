#!/usr/bin/python3
"""Defines the views of handling cities in the API"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage, storage_t
from models.state import State
from models.city import City
from models.state import State
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'])
@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'])
def city_handler(state_id=None, city_id=None):
    """Handler function for the cities endpoint"""
    handlers = {
            'GET': getCities,
            'DELETE': deleteCities,
            'POST': postCities,
            'PUT': putCities
    }
    if request.method in handlers:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getCities(state_id=None, city_id=None):
    """Gets and retrieves all cities or a city based on ID"""
    if state_id:
        state_list = storage.get(State, state_id)
        if state_list:
            cty_in_sts = list(map(lambda x: x.to_dict(), state_list.cities))
            return make_response(jsonify(cty_in_sts))
    elif city_id:
        city_list = storage.get(City, city_id)
        if city_list:
            return make_response(jsonify(city_list.to_dict()))
    raise NotFound()


def deleteCities(state_id=None, city_id=None):
    """Deletes a state object based on ID"""
    if city_id:
        city_list = storage.get(City, city_id)
        if city_list:
            storage.delete(city_list)
            storage.save()
            return make_response(jsonify({}), 200)
    raise NotFound()


def postCities(state_id=None, city_id=None):
    """Posts or adds a new city to the object list"""
    state_list = storage.get(State, state_id)
    if not state_list:
        raise NotFound()
    city_data = request.get_json()
    if type(city_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in city_data:
        raise BadRequest(description="Missing name")
    city_data["state_id"] = state_id
    created_city = City(**city_data)
    created_city.save()
    return make_response(jsonify(created_city.to_dict()), 201)


def putCities(state_id=None, city_id=None):
    """Puts or updates a state based on ID"""
    immut_attrs = ("id", "state_id", "created_id", "updated_at")
    if city_id:
        city_list = storage.get(City, city_id)
        if city_list:
            city_data = request.get_json()
            if type(city_data) is not dict:
                raise BadRequest(description="Not a JSON")
            for key, value in city_data.items():
                if key not in immut_attrs:
                    setattr(city_list, key, value)
            city_list.save()
            return make_response(jsonify(city_list.to_dict()), 200)
    raise NotFound()
