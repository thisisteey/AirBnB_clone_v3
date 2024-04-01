#!/usr/bin/python3
"""Defines the views of handling states in the API"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.state import State
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/states", methods=['GET', 'POST'])
@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'])
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
            return make_response(jsonify(state_list[0].to_dict()), 200)
        raise NotFound()
    state_objs = list(map(lambda x: x.to_dict(), state_objs))
    return make_response(jsonify(state_objs))


def deleteStates(state_id=None):
    """Delete a state object based on ID"""
    state_objs = storage.all(State).values()
    state_list = list(filter(lambda x: x.id == state_id, state_objs))
    if state_list:
        storage.delete(state_list[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def postStates(state_id=None):
    """Posts or adds a new state to the object list"""
    state_data = request.get_json()
    if type(state_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in state_data:
        raise BadRequest(description="Missing name")
    created_state = State(**state_data)
    created_state.save()
    return make_response(jsonify(created_state.to_dict()), 201)


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
        return make_response(jsonify(prev_state.to_dict()), 200)
    raise NotFound()
