#!/usr/bin/python3
"""Index view of the API of the web application"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def getStatus():
    """Gets and returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def getStats():
    """Gets and returns the number of objects based off type"""
    obj_types = {
            "amenities": 'Amenity',
            "cities": 'City',
            "places": 'Place',
            "reviews": 'Review',
            "states": 'State',
            "users": 'User'
    }
    for key, val in obj_types.items():
        obj_types[key] = storage.count(val)
    return jsonify(obj_types)
