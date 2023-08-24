#!/usr/bin/python3
"""Routes module for api"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Returns a JSON of the status of the server"""
    return jsonify({"status": "OK"})
