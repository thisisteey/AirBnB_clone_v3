#!/usr/bin/python3
"""The Flask web application API for the AirBnB"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""Instance of the Flask web application"""
app_host = getenv("HBNB_API_HOST", default="0.0.0.0")
app_port = int(getenv("HBNB_API_PORT", default=5000))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": app_host}})


@app.teardown_appcontext
def close_storage(exception):
    """Closes SQLAlchemy connection in Flask context"""
    storage.close()


@app.errorhandler(404)
def page_404_error(error):
    """Handles page not found error 404"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host=app_host, port=app_port, threaded=True)
