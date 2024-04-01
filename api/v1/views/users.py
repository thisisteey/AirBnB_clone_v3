#!/usr/bin/python3
"""Defines the views of handling users in the API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/users", methods=['GET', 'POST'])
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'])
def user_handler(user_id=None):
    """Handler function for the users endpoint"""
    handlers = {
            'GET': getUsers,
            'DELETE': deleteUsers,
            'POST': postUsers,
            'PUT': putUsers
    }
    if request.method in handlers:
        return handlers[request.method](user_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getUsers(user_id=None):
    """Gets and retrieves all users or a user based on ID"""
    user_objs = storage.all(User).values()
    if user_id:
        user_list = list(filter(lambda x: x.id == user_id, user_objs))
        if user_list:
            return make_response(jsonify(user_list[0].to_dict()))
        raise NotFound()
    user_objs = list(map(lambda x: x.to_dict(), user_objs))
    return make_response(jsonify(user_objs))


def deleteUsers(user_id=None):
    """Delete a user object based on ID"""
    user_objs = storage.all(User).values()
    user_list = list(filter(lambda x: x.id == user_id, user_objs))
    if user_list:
        storage.delete(user_list[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def postUsers(user_id=None):
    """Posts or adds a new user to the object list"""
    user_data = request.get_json()
    if type(user_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "email" not in user_data:
        raise BadRequest(description="Missing email")
    if "password" not in user_data:
        raise BadRequest(description="Missing password")
    created_user = User(**user_data)
    created_user.save()
    return make_response(jsonify(created_user.to_dict()), 201)


def putUsers(user_id=None):
    """Puts or updates a user based on ID"""
    immut_attrs = ("id", "email", "created_at", "updated_at")
    user_objs = storage.all(User).values()
    user_list = list(filter(lambda x: x.id == user_id, user_objs))
    if user_list:
        user_data = request.get_json()
        if type(user_data) is not dict:
            raise BadRequest(description="Not a JSON")
        prev_user = user_list[0]
        for key, value in user_data.items():
            if key not in immut_attrs:
                setattr(prev_user, key, value)
        prev_user.save()
        return make_response(jsonify(prev_user.to_dict()), 200)
    raise NotFound()
