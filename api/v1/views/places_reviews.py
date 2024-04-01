#!/usr/bin/python3
"""Defines the views of handling reviews in the API"""
from json import dumps
from api.v1.views import app_views
from flask import Response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest


HTTP_METHODS = ["GET", "DELETE", "POST", "PUT"]
"""HTTP methods supported for the reviews endpoint"""


@app_views.route("/places/place_id/reviews", methods=HTTP_METHODS)
@app_views.route("/reviews/<review_id>", methods=HTTP_METHODS)
def review_handler(place_id=None, review_id=None):
    """Handler function for the reviews endpoint"""
    handlers = {
            'GET': getReviews,
            'DELETE': deleteReviews,
            'POST': postReviews,
            'PUT': putReviews
    }
    if request.method in handlers:
        return handlers[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def getReviews(place_id=None, review_id=None):
    """Gets and retrieves all reviews or a review based on ID"""
    if place_id:
        place_objs = storage.get(Place, place_id)
        if place_objs:
            review_list = []
            for revs in place_objs.reviews:
                review_list.append(revs.to_dict())
            res_data = dumps(review_list, indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    elif review_id:
        review_objs = storage.get(Review, review_id)
        if review_objs:
            res_data = dumps(review_objs.to_dict(), indent=2)
            return Response(res_data,
                            content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')


def deleteReviews(place_id=None, review_id=None):
    """Delete a review object based on ID"""
    review_objs = storage.get(Review, review_id)
    if review_objs:
        storage.delete(review_objs)
        storage.save()
        res_data = dumps({}, indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')


def postReviews(place_id=None, review_id=None):
    """Posts or adds a new review to the object list"""
    place_objs = storage.get(Place, place_id)
    if not place_objs:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
    review_data = request.get_json()
    if type(review_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "user_id" not in review_data:
        raise BadRequest(description="Missing user_id")
    user_objs = storage.get(User, review_data['user_id'])
    if not user_objs:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
    if "text" not in review_data:
        raise BadRequest(description="Missing text")
    review_data['place_id'] = place_id
    created_review = Review(**review_data)
    created_review.save()
    res_data = dumps(created_review.to_dict(), indent=2)
    return Response(res_data, status=201,
                    content_type='application/json; charset=utf-8')


def putReviews(place_id=None, review_id=None):
    """Puts or updates a review based on ID"""
    immut_attrs = ("id", "user_id", "place_id", "created_at", "updated_at")
    review_objs = storage.get(Review, review_id)
    if review_objs:
        review_data = request.get_json()
        if type(review_data) is not dict:
            raise BadRequest(description="Not a JSON")
        for key, value in review_data.items():
            if key not in immut_attrs:
                setattr(review_objs, key, value)
        review_objs.save()
        res_data = dumps(review_objs.to_dict(), indent=2)
        return Response(res_data, status=200,
                        content_type='application/json; charset=utf-8')
    else:
        errmsg = {"error": "Not found"}
        res_data = dumps(errmsg, indent=2)
        return Response(res_data,
                        content_type='application/json; charset=utf-8')
