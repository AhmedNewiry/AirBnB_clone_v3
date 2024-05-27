#!/usr/bin/python3
"""Create a new view for State objects that
   handles all default RESTFul API actions
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, make_response, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieve the list of all states"""
    states = storage.all(State).values()
    return make_response(jsonify([state.to_dict() for
                         state in states.values()]), 200)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """retrieve one state by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return make_response(jsonify({state.to_dict}), 200)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """adds a new object to the database"""
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    state = State(**body)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state object"""
    state = storage.get(State, state_id)
        if not state:
    abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    ignored_values = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_values:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
