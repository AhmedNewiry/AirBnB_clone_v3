#!/usr/bin/python3
"""a module containing the routes of cities view"""

from api.v1.views import app_views
from models import storage
from flask import make_response, request, abort, jsonify
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """Adds a new City object to the storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, description="Not a JSON")
    if 'name' not in city_data:
        abort(400, description="Missing name")
    city_data['state_id'] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")
    ignored_values = {'id', 'state_id', 'created_at', 'updated_at'}
    for key, value in body.items():
        if key not in ignored_values:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
