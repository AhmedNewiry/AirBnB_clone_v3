#!/usr/bin/python3
""" a module containing mutual views routes"""


from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from models import storage
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def index():
    """handles the /status route"""
    return make_response(jsonify({"status": 'OK'}), 200)


@app_views.route('/stats', methods=['GET'])
def status():
    """an endpoint that retrieves
       the number of each objects
    """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    res = {}
    for key, value in classes.items():
        res[key] = storage.count(value)
    return make_response(jsonify(res), 200)
