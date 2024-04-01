#!/usr/bin/python3
"""Defines the views of handling amenities in the API"""
from json import dumps
from api.v1.views import app_views
from flask import Response, request
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import MethodNotAllowed, BadRequest


HTTP_METHODS = ["GET", "DELETE", "POST", "PUT"]
"""HTTP methods supported for the amenities endpoint"""


@app_views.route("/amenities", methods=HTTP_METHODS)
@app_views.route("/amenities/<amenity_id>", methods=HTTP_METHODS)
def amenity_handler(amenity_id=None):
    """Handler function for the amenities endpoint"""
    handlers = {
            'GET': getAmenities,
            'DELETE': deleteAmenities,
            'POST': postAmenities,
            'PUT': putAmenities
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getAmenities(amenity_id=None):
    """Gets and retrieves all amenities or a amenity based on ID"""
    amenity_objs = storage.all(Amenity).values()
    if amenity_id:
        amenity_list = list(filter(lambda x: x.id == amenity_id, amenity_objs))
        if amenity_list:
            amenity_dict = amenity_list[0].to_dict()
            res_data = dumps(amenity_dict, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
        else:
            errmsg = {"error": "Not found"}
            res_data = dumps(errmsg, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    amenity_objs = list(map(lambda x: x.to_dict(), amenity_objs))
    res_data = dumps(amenity_objs, indent=2)
    return Response(res_data, content_type='application/json; charset=utf-8')


def deleteAmenities(amenity_id=None):
    """Delete a amenity object based on ID"""
    amenity_objs = storage.all(Amenity).values()
    amenity_list = list(filter(lambda x: x.id == amenity_id, amenity_objs))
    if amenity_list:
        storage.delete(amenity_list[0])
        storage.save()
        res_data = dumps({}, indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')


def postAmenities(amenity_id=None):
    """Posts or adds a new amenity to the object list"""
    amenity_data = request.get_json()
    if type(amenity_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in amenity_data:
        raise BadRequest(description="Missing name")
    created_amenity = Amenity(**amenity_data)
    created_amenity.save()
    res_data = dumps(created_amenity.to_dict(), indent=2)
    return Response(res_data, status=201,
                    content_type='application/json; charset=utf-8')


def putAmenities(amenity_id=None):
    """Puts or updates a amenity based on ID"""
    immut_attrs = ("id", "created_at", "updated_at")
    amenity_objs = storage.all(Amenity).values()
    amenity_list = list(filter(lambda x: x.id == amenity_id, amenity_objs))
    if amenity_list:
        amenity_data = request.get_json()
        if type(amenity_data) is not dict:
            raise BadRequest(description="Not a JSON")
        prev_amenity = amenity_list[0]
        for key, value in amenity_data.items():
            if key not in immut_attrs:
                setattr(prev_amenity, key, value)
        prev_amenity.save()
        res_data = dumps(prev_amenity.to_dict(), indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
