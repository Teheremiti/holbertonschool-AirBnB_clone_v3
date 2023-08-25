#!/usr/bin/python3
"""View API for Amenity"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """Get the list of all Amenity objects"""
    amenities_list = []
    for amenity in storage.all(Amenity).values():
        amenities_list.append(amenity)
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """Get the Amenity object matching amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes the Amenity object matching amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    http_request = request.get_json(silent=False)
    if not http_request:
        abort(400, description="Not a JSON")
    elif "name" not in http_request:
        abort(400, description="Missing name")

    new_amenity = Amenity(name=http_request["name"])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the Amenity object matching amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    http_request = request.get_json(silent=False)
    if not http_request:
        abort(400, description="Not a JSON")

    for attr, value in http_request.items():
        if attr not in ['id', 'created_at', 'updated_at']:
            amenity[attr] = value

    storage.save()
    return jsonify(amenity.to_dict()), 200
