#!/usr/bin/python3
"""View API for City"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities(state_id):
    """List all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities_list = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """Return the City object associated to city_id"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(city_id):
    """Delete a City object by id"""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    http_request = request.get_json(silent=True)
    if not http_request:
        return "Not a JSON\n", 400
    elif "name" not in http_request:
        return "Missing name\n", 400

    new_city = City(name=http_request["name"], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates the City matching the id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    http_request = request.get_json(silent=True)
    if not http_request:
        abort(400, description="Not a JSON")

    for attr, value in http_request.items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(city, attr, value)

    storage.save()
    return jsonify(city.to_dict()), 200
