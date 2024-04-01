#!/usr/bin/python3
"""Defines the views of handling place_amenities in the API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/places/place_id/amenities", methods=['GET'])
@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE', 'POST'])
def places_amenities_handler(place_id=None, amenity_id=None):
    """Handler function for the places_amenities endpoint"""
    handlers = {
            'GET': getPlaces_Amenities,
            'DELETE': deletePlaces_Amenities,
            'POST': postPlaces_Amenities
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getPlaces_Amenities(place_id=None, amenity_id=None):
    """Gets and retrieves the amenity or amenities of a place based on ID"""
    if place_id:
        place_objs = storage.get(Place, place_id)
        if place_objs:
            amenities_list = list(map(lambda x: x.to_dict(),
                                      place_objs.amenities))
            return make_response(jsonify(amenities_list))
    raise NotFound()


def deletePlaces_Amenities(place_id=None, amenity_id=None):
    """Deletes an amenity from a place based on ID"""
    if place_id and amenity_id:
        place_objs = storage.get(Place, place_id)
        amenity_objs = storage.get(Amenity, amenity_id)
        if not place_objs or not amenity_objs:
            raise NotFound()
        place_link_amenity = list(
                filter(lambda x: x.id == amenity_id, place_objs.amenities)
        )
        if not place_link_amenity:
            raise NotFound()
        if storage_t == 'db':
            amenity_link_place = list(
                    filter(lambda x: x.id == place_id,
                           amenity_objs.place_amenites)
            )
            if not amenity_link_place:
                raise NotFound()
            place_objs.amenities.remove(amenity_objs)
            place_objs.save()
            return make_response(jsonify({}), 200)
        else:
            amenity_idx = place_objs.amenity_ids.index(amenity_id)
            place_objs.amenity_ids.pop(amenity_idx)
            place_objs.save()
            return make_response(jsonify({}), 200)
    raise NotFound()


def postPlaces_Amenities(place_id=None, amenity_id=None):
    """Posts or adds an amenity from a place based on ID"""
    if place_id and amenity_id:
        place_objs = storage.get(Place, place_id)
        amenity_objs = storage.get(Amenity, amenity_id)
        if not place_objs or not amenity_objs:
            raise NotFound()
        if storage_t == 'db':
            place_link_amenity = list(
                    filter(lambda x: x.id == amenity_id, place_objs.amenities)
            )
            amenity_link_place = list(
                    filter(lambda x: x.id == place_id,
                           amenity_objs.place_amenites)
            )
            if amenity_link_place and place_link_amenity:
                amenity_dict = amenity_objs.to_dict()
                del amenity_dict['place_amenities']
                return make_response(jsonify(amenity_dict), 200)
            place_objs.amenities.append(amenity_objs)
            place_objs.save()
            amenity_dict = amenity_objs.to_dict()
            del amenity_dict['place_amenities']
            return make_response(jsonify(amenity_dict), 201)
        else:
            if amenity_id in place_objs.amenity_ids:
                return make_response(jsonify(amenity_objs.to_dict()), 200)
            place_objs.amenity_ids.push(amenity_id)
            place_objs.save()
            return make_response(jsonify(amenity_objs.to_dict()), 201)
    raise NotFound()
