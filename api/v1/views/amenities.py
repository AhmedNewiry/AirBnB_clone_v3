#!/usr/bin/python3
"""a module containing amenities routes"""

from api.v1.views import app_views
from models import storage
from flask import make_response, request, abort, jsonify
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return make_response(jsonify([amenity.to_dict()
                         for amenity in amenities]), 200)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(400)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity_id(amenity_id):
    """deletes an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """creates an amenity object"""
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    amenity = Amenity(**body)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    ignored_values = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_values:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
