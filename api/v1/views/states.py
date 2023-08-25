#!/usr/bin/python3
"""View API for State"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """List all State objects"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Return the State object associated to state_id"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)
    

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Delete a State by id"""
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    http_request = request.get_json(silent=True)
    if not http_request:
        return "Not a JSON\n", 400
    elif "name" not in http_request:
        return "Missing name\n", 400
    new_state = State(name=http_request["name"])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates the State matching the id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    http_request = request.get_json(silent=True)
    if not http_request:
        return jsonify({"error": "Not a JSON"}), 400

    for attr, value in http_request.items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, value)

    storage.save()
    return jsonify(state.to_dict()), 200
