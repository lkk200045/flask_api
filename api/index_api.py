# -*- coding: utf-8 -*-
import logging
from flask import Blueprint
from flask import json

logger = logging.getLogger("application")

index_api = Blueprint("index_api", __name__)


@index_api.route("/isalive", methods=["POST", "GET"])
def isalive():
    return json.jsonify("hello")
