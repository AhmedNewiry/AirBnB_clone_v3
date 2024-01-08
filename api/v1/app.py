#!/usr/bin/python3
""" a module for flask application"""

import os
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(err):
    """closes the connection to the database"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')), threaded=True)
