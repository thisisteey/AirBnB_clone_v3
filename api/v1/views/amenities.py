#!/usr/bin/python3
"""Defines the views of handling amenities in the API"""
from api.v1.views import app_views
from flask import make_response, jsonify, request
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/amenities", methods=['GET', 'POST'])
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'POST'])
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
            return make_response(jsonify(amenity_list[0].to_dict()))
        raise NotFound()
    amenity_objs = list(map(lambda x: x.to_dict(), amenity_objs))
    return make_response(jsonify(amenity_objs))


def deleteAmenities(amenity_id=None):
    """Delete a amenity object based on ID"""
    amenity_objs = storage.all(Amenity).values()
    amenity_list = list(filter(lambda x: x.id == amenity_id, amenity_objs))
    if amenity_list:
        storage.delete(amenity_list[0])
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def postAmenities(amenity_id=None):
    """Posts or adds a new amenity to the object list"""
    amenity_data = request.get_json()
    if type(amenity_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "name" not in amenity_data:
        raise BadRequest(description="Missing name")
    created_amenity = Amenity(**amenity_data)
    created_amenity.save()
    return make_response(jsonify(created_amenity.to_dict()), 201)


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
        return make_response(jsonify(prev_amenity.to_dict()), 200)
    raise NotFound()
