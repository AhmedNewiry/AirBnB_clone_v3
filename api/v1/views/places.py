#!/usr/bin/python3
"""Create a new view for Place objects that
   handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from flask import make_response, request, abort, jsonify
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places = storage.all('Place')
    req_places = []
    for place in places:
        place.city_id = city_id.to_dict()
        req_places.append(place)

    return make_response(jsonify(req_places), 200)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """retrieves a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """deletes a place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def add_place(city_id):
    """ Creates a Place object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if "user_id" not in body:
        abort(400, "Missing user_id")
    user_id = body["user_id"]
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if "name" not in body:
        abort(400, "Missing name")
    place = Place(**body)
    setattr(place, "city_id", city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place_id(place_id):
    """updates a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
