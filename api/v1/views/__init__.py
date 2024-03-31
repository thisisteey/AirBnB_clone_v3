#!/usr/bin/python3
"""The blueprint of the Flask web application API"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
"""API blueprint of the AirBnB web application"""


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
