#!/usr/bin/python3
"""Defines the views of handling place_amenities in the API"""
from json import dumps
from api.v1.views import app_views
from flask import Response, request
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from werkzeug.exceptions import MethodNotAllowed, BadRequest


HTTP_METHODS = ["GET", "DELETE", "POST"]
"""HTTP methods supported for the place_amenities endpoint"""


@app_views.route("/places/place_id/amenities", methods=HTTP_METHODS)
@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=HTTP_METHODS)
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
            res_data = dumps(amenities_list, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')


def deletePlaces_Amenities(place_id=None, amenity_id=None):
    """Deletes an amenity from a place based on ID"""
    if place_id and amenity_id:
        place_objs = storage.get(Place, place_id)
        amenity_objs = storage.get(Amenity, amenity_id)
        if not place_objs or not amenity_objs:
            errmsg = {"error": "Not found"}
            res_data = dumps(res_data, indent=2)
            return Response(res_data, status=404,
                            content_type='application/json; charset=utf-8')
        place_link_amenity = list(
                filter(lambda x: x.id == amenity_id, place_objs.amenities)
        )
        if not place_link_amenity:
            errmsg = {"error": "Not found"}
            res_data = dumps(res_data, indent=2)
            return Response(res_data, status=404,
                            content_type='application/json; charset=utf-8')
        if storage_t == 'db':
            amenity_link_place = list(
                    filter(lambda x: x.id == place_id,
                           amenity_objs.place_amenites)
            )
            if not amenity_link_place:
                errmsg = {"error": "Not found"}
                res_data = dumps(res_data, indent=2)
                return Response(res_data, status=404,
                                content_type='application/json; charset=utf-8')
            place_objs.amenities.remove(amenity_objs)
            place_objs.save()
            res_data = dumps({}, indent=2)
            return Response(res_data, status=200,
                            content_type='application/json; charset=utf-8')
        else:
            amenity_idx = place_objs.amenity_ids.index(amenity_id)
            place_objs.amenity_ids.pop(amenity_idx)
            place_objs.save()
            res_data = dumps({}, indent=2)
            return Response(res_data, status=200,
                            content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data, status=404,
                        content_type='application/json; charset=utf-8')


def postPlaces_Amenities(place_id=None, amenity_id=None):
    """Posts or adds an amenity from a place based on ID"""
    if place_id and amenity_id:
        place_objs = storage.get(Place, place_id)
        amenity_objs = storage.get(Amenity, amenity_id)
        if not place_objs or not amenity_objs:
            errmsg = {"error": "Not found"}
            res_data = dumps(res_data, indent=2)
            return Response(res_data, status=404,
                            content_type='application/json; charset=utf-8')
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
                res_data = dumps(amenity_dict, indent=2)
                return Response(res_data, status=200,
                                content_type='application/json; charset=utf-8')
            place_objs.amenities.append(amenity_objs)
            place_objs.save()
            amenity_dict = amenity_objs.to_dict()
            del amenity_dict['place_amenities']
            res_data = dumps(amenity_dict, indent=2)
            return Response(res_data, status=201,
                            content_type='application/json; charset=utf-8')
        else:
            if amenity_id in place_objs.amenity_ids:
                res_data = dumps(amenity_objs.to_dict(), indent=2)
                return Response(res_data, status=200,
                                content_type='application/json; charset=utf-8')
            place_objs.amenity_ids.push(amenity_id)
            place_objs.save()
            res_data = dumps(amenity_objs.to_dict(), indent=2)
            return Response(res_data, status=201,
                            content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data, status=404,
                        content_type='application/json; charset=utf-8')
