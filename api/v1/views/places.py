#!/usr/bin/python3
"""Defines the views of handling places in the API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/cities/city_id/places", methods=['GET', 'POST'])
@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'])
def place_handler(city_id=None, place_id=None):
    """Handler function for the places endpoint"""
    handlers = {
            'GET': getPlaces,
            'DELETE': deletePlaces,
            'POST': postPlaces,
            'PUT': putPlaces
    }
    if request.method in handlers:
        return handlers[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getPlaces(city_id=None, place_id=None):
    """Gets and retrieves all places or a place based on ID"""
    if city_id:
        city_objs = storage.get(City, city_id)
        if city_objs:
            place_list = list(city_objs.places)
            place_dict = list(map(lambda x: x.to_dict(), place_list))
            return make_response(jsonify(place_dict), 200)
        raise NotFound()
    elif place_id:
        place_objs = storage.get(Place, place_id)
        if place_objs:
            return make_response(jsonify(place_objs.to_dict()), 200)
        raise NotFound()
    raise NotFound()


def deletePlaces(city_id=None, place_id=None):
    """Delete a place object based on ID"""
    if place_id:
        place_objs = storage.get(Place, place_id)
        if place_objs:
            storage.delete(place_objs)
            storage.save()
            return make_response(jsonify({}), 200)
    raise NotFound()


def postPlaces(city_id=None, place_id=None):
    """Posts or adds a new place to the object list"""
    city_objs = storage.get(City, city_id)
    if not city_objs:
        raise NotFound()
    place_data = request.get_json()
    if type(place_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "user_id" not in place_data:
        raise BadRequest(description="Missing user_id")
    user_objs = storage.get(User, place_data['user_id'])
    if not user_objs:
        raise NotFound()
    if "name" not in place_data:
        raise BadRequest(description="Missing name")
    place_data['city_id'] = city_id
    created_place = Place(**place_data)
    created_place.save()
    return make_response(jsonify(created_place.to_dict()), 201)


def putPlaces(city_id=None, place_id=None):
    """Puts or updates a place based on ID"""
    immut_attrs = ("id", "user_id", "city_id", "created_at", "updated_at")
    place_objs = storage.get(Place, place_id)
    if place_objs:
        place_data = request.get_json()
        if type(place_data) is not dict:
            raise BadRequest(description="Not a JSON")
        for key, value in place_data.items():
            if key not in immut_attrs:
                setattr(place_objs, key, value)
        place_objs.save()
        return make_response(jsonify(place_objs.to_dict()), 200)
    raise NotFound()


@app_views.route("/places_search", methods=['POST'])
def postPlaces_Search():
    """Posts or adds a place based on the IDs of state, city or amenity"""
    reqdata = request.get_json()
    if type(reqdata) is not dict:
        raise BadRequest(description="Not a JSON")
    places_objs = storage.all(Place).values()
    places = []
    places_id = []
    data_stat = (
            all([
                "states" in reqdata and type(reqdata["states"]) is list,
                "states" in reqdata and len(reqdata["states"])
            ]),
            all([
                "cities" in reqdata and type(reqdata["cities"]) is list,
                "cities" in reqdata and len(reqdata["cities"])
            ]),
            all([
                "amenities" in reqdata and type(reqdata["amenities"]) is list,
                "amenities" in reqdata and len(reqdata["amenities"])
            ])
    )
    if data_stat[0]:
        for state_id in reqdata["states"]:
            if not state_id:
                continue
            state_objs = storage.get(State, state_id)
            if not state_objs:
                continue
            for city_objs in state_objs.cities:
                filt_places = []
                if storage_t == 'db':
                    filt_places = list(
                            filter(lambda x: x.id not in places_id,
                                   city_objs.places)
                    )
                else:
                    filt_places = []
                    for place in places_objs:
                        if place.id in places_id:
                            continue
                        if place.city_id == city_objs.id:
                            filt_places.append(place)
                places.extend(filt_places)
                places_id.extend(list(map(lambda x: x.id, filt_places)))
    if data_stat[1]:
        for city_id in reqdata["cities"]:
            if not city_id:
                continue
            city_objs = storage.get(City, city_id)
            if city_objs:
                filt_places = []
                if storage_t == 'db':
                    filt_places = list(
                            filter(lambda x: x.id not in places_id,
                                   city_objs.places)
                    )
                else:
                    filt_places = []
                    for place in places_objs:
                        if place.id in places_id:
                            continue
                        if place.city_id == city_objs.id:
                            filt_places.append(place)
                places.extend(filt_places)
    del places_id
    if all([not data_stat[0], not data_stat[1]]) or not reqdata:
        places = places_objs
    if data_stat[2]:
        amenity_ids = []
        for amenity_id in reqdata["amenities"]:
            if not amenity_id:
                continue
            amenity_objs = storage.get(Amenity, amenity_id)
            if amenity_objs and amenity.id not in amenity_ids:
                amenity_ids.append(amenity_objs.id)
        del_places = []
        for place in places:
            place_amenities_ids = list(map(lambda x: x.id, place.amenities))
            if not amenity_ids:
                continue
            for amenity_id in amenity_ids:
                if amenity_id not in place_amenities_ids:
                    del_places.append(place.id)
                    break
        places = list(filter(lambda x: x.id not in del_places, places))
    places_data = []
    for place in places:
        place_dict = place.to_dict()
        if "amenities" in place_dict:
            del place_dict["amenities"]
        places_data.append(place_dict)
    return make_response(jsonify(places_data))
