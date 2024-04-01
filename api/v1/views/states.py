#!/usr/bin/python3
"""Defines the views of handling states in the API"""
from json import dumps
from api.v1.views import app_views
from flask import Response, request
from models import storage
from models.state import State
from werkzeug.exceptions import MethodNotAllowed, BadRequest


HTTP_METHODS = ["GET", "DELETE", "POST", "PUT"]
"""HTTP methods supported for the states endpoint"""


@app_views.route("/states", methods=HTTP_METHODS)
@app_views.route("/states/<state_id>", methods=HTTP_METHODS)
def state_handler(state_id=None):
    """Handler function for the states endpoint"""
    handlers = {
            'GET': getStates,
            'DELETE': deleteStates,
            'POST': postStates,
            'PUT': putStates
    }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getStates(state_id=None):
    """Gets and retrieves all states or a state based on ID"""
    state_objs = storage.all(State).values()
    if state_id:
        state_list = list(filter(lambda x: x.id == state_id, state_objs))
        if state_list:
            state_dict = state_list[0].to_dict()
            res_data = dumps(state_dict, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
        else:
            errmsg = {"error": "Not found"}
            res_data = dumps(errmsg, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    state_objs = list(map(lambda x: x.to_dict(), state_objs))
    res_data = dumps(state_objs, indent=2)
    return Response(res_data, content_type='application/json; charset=utf-8')


def deleteStates(state_id=None):
    """Delete a state object based on ID"""
    state_objs = storage.all(State).values()
    state_list = list(filter(lambda x: x.id == state_id, state_objs))
    if state_list:
        storage.delete(state_list[0])
        storage.save()
        res_data = dumps({}, indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')


def postStates(state_id=None):
    """Posts or adds a new state to the object list"""
    state_data = request.get_json()
    if type(state_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in state_data:
        raise BadRequest(description="Missing name")
    created_state = State(**state_data)
    created_state.save()
    res_data = dumps(created_state.to_dict(), indent=2)
    return Response(res_data, status=201,
                    content_type='application/json; charset=utf-8')


def putStates(state_id=None):
    """Puts or updates a state based on ID"""
    immut_attrs = ("id", "created_at", "updated_at")
    state_objs = storage.all(State).values()
    state_list = list(filter(lambda x: x.id == state_id, state_objs))
    if state_list:
        state_data = request.get_json()
        if type(state_data) is not dict:
            raise BadRequest(description="Not a JSON")
        prev_state = state_list[0]
        for key, value in state_data.items():
            if key not in immut_attrs:
                setattr(prev_state, key, value)
        prev_state.save()
        res_data = dumps(prev_state.to_dict(), indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
