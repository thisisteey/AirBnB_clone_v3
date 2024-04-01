#!/usr/bin/python3
"""Defines the views of handling reviews in the API"""
from api.v1.views import app_views
from flask import make_response, request, jsonify
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from werkzeug.exceptions import MethodNotAllowed, BadRequest, NotFound


@app_views.route("/places/place_id/reviews", methods=['GET', 'POST'])
@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'])
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
            reveiw_dict = [review.to_dict() for review in place_objs.reviews]
            return make_response(jsonify(review_dict))
        raise NotFound()
    elif review_id:
        review_objs = storage.get(Review, review_id)
        if review_objs:
            return make_response(jsonify(review_objs.to_dict()))
        raise NotFound()
    raise NotFound()


def deleteReviews(place_id=None, review_id=None):
    """Delete a review object based on ID"""
    review_objs = storage.get(Review, review_id)
    if review_objs:
        storage.delete(review_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    raise NotFound()


def postReviews(place_id=None, review_id=None):
    """Posts or adds a new review to the object list"""
    place_objs = storage.get(Place, place_id)
    if not place_objs:
        raise NotFound()
    review_data = request.get_json()
    if type(review_data) is not dict:
        raise BadRequest(description="Not a JSON")
    if "user_id" not in review_data:
        raise BadRequest(description="Missing user_id")
    user_objs = storage.get(User, review_data['user_id'])
    if not user_objs:
        raise NotFound()
    if "text" not in review_data:
        raise BadRequest(description="Missing text")
    review_data['place_id'] = place_id
    created_review = Review(**review_data)
    created_review.save()
    return make_response(jsonify(created_review.to_dict()), 201)


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
        return make_response(jsonify(review_objs.to_dict()), 200)
    raise NotFound()
