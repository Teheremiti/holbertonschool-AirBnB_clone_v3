#!/usr/bin/python3
"""Routes module for api"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Returns a JSON of the status of the server"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Returns the number of objects by type"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    counts = {}
    for type, cls in classes.items():
        counts[type] = storage.count(cls)
    return jsonify(counts)
