#!/usr/bin/python3
"""Defines the views of handling users in the API"""
from json import dumps
from api.v1.views import app_views
from flask import Response, request
from models import storage
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest


HTTP_METHODS = ["GET", "DELETE", "POST", "PUT"]
"""HTTP methods supported for the users endpoint"""


@app_views.route("/users", methods=HTTP_METHODS)
@app_views.route("/users/<user_id>", methods=HTTP_METHODS)
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
            user_dict = user_list[0].to_dict()
            res_data = dumps(user_dict, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
        else:
            errmsg = {"error": "Not found"}
            res_data = dumps(errmsg, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    user_objs = list(map(lambda x: x.to_dict(), user_objs))
    res_data = dumps(user_objs, indent=2)
    return Response(res_data, content_type='application/json; charset=utf-8')


def deleteUsers(user_id=None):
    """Delete a user object based on ID"""
    user_objs = storage.all(User).values()
    user_list = list(filter(lambda x: x.id == user_id, user_objs))
    if user_list:
        storage.delete(user_list[0])
        storage.save()
        res_data = dumps({}, indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')


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
    res_data = dumps(created_user.to_dict(), indent=2)
    return Response(res_data, status=201,
                    content_type='application/json; charset=utf-8')


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
        res_data = dumps(prev_user.to_dict(), indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
