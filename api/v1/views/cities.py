#!/usr/bin/python3
"""Defines the views of handling cities in the API"""
from json import dumps
from api.v1.views import app_views
from flask import Response, request
from models import storage
from models.state import State
from models.city import City
from werkzeug.exceptions import MethodNotAllowed, BadRequest


HTTP_METHODS = ["GET", "DELETE", "POST", "PUT"]
"""HTTP methods supported for the states endpoint"""


@app_views.route("/states/<state_id>/cities", methods=HTTP_METHODS)
@app_views.route("/cities/<city_id>", methods=HTTP_METHODS)
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
            res_data = dumps(cty_in_sts, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    elif city_id:
        city_list = storage.get(City, city_id)
        if city_list:
            res_data = dumps(city_list.to_dict(), indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    errmsg = {"error": "Not found"}
    res_data = dumps(errmsg, indent=2)
    return Response(res_data, content_type='application/json; charset=utf-8')


def deleteCities(state_id=None, city_id=None):
    """Deletes a state object based on ID"""
    if city_id:
        city_list = storage.get(City, city_id)
        if city_list:
            storage.delete(city_list)
            storage.save()
            res_data = dumps({}, indent=2)
            return Response(res_data, status=200,
                            content_type='application/json; charset=utf-8')
    errmsg = {"error": "Not found"}
    res_data = dumps(errmsg, indent=2)
    return Response(res_data, content_type='application/json; charset=utf-8')


def postCities(state_id=None, city_id=None):
    """Posts or adds a new city to the object list"""
    state_list = storage.get(State, state_id)
    if not state_list:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
    city_data = request.get_json()
    if type(city_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in city_data:
        raise BadRequest(description="Missing name")
    city_data["state_id"] = state_id
    created_city = City(**city_data)
    created_city.save()
    res_data = dumps(created_city.to_dict(), indent=2)
    return Response(res_data, status=201,
                    content_type='application/json; charset=utf-8')


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
            res_data = dumps(city_list.to_dict(), indent=2)
            return Response(res_data, status=200,
                            content_type='application/json; charset=utf-8')
    errmsg = {"error": "Not found"}
    res_data = dumps(errmsg, indent=2)
    return Response(res_data, content_type='application/json; charset=utf-8')
