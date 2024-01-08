#!/usr/bin/python3
"""a module containing the routes of cities view"""

from api.v1.views import app_views
from models import storage
from flask import make_response, request, abort, jsonify
from models.city import City


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """retrieves the list of all City objects of a State"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    cities = storage.all('City')
    req_cities = []
    for city in cities:
        if city.state_id == state_id:
            req_cities.append(city.to_dict())
    return make_response(jsonify(req_cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    city = City(**city)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """adds a new object to the storage"""
    city = request.get_json()
    if not city:
        abort(400, 'Not a JSON')
    if 'name' not in city:
        abort(400, 'Missing name')
    state = storage.get('State', state_id)
    if not state:
        abort(400)
    new_city = City(**city)
    setarr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a city object"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    ignored_values = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_values:
            setarr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict), 200)
