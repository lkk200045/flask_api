# -*- coding: utf-8 -*-
import argparse
import logging
from flask import Flask
from flask_cors import CORS
from config.application import app_context
from api.index_api import index_api
from api.field_api import field_api
from api.storage_api import storage_api
from api.generic_api import generic_api

HOST = app_context.host
PORT = app_context.port
PREFIX = app_context.context_path + "/" + app_context.api_path_name
API_VERSION = app_context.api_version
URL_PREFIX = PREFIX + "/" + API_VERSION

logger = logging.getLogger("application")


def create_flask_app():
    app = Flask(app_context.application_name)
    CORS(app)

    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    app.config["JSON_AS_ASCII"] = False
    app.config["app_context"] = app_context

    app.register_blueprint(index_api, url_prefix=URL_PREFIX)
    app.register_blueprint(field_api, url_prefix=URL_PREFIX)
    app.register_blueprint(storage_api, url_prefix=URL_PREFIX)
    app.register_blueprint(generic_api, url_prefix=URL_PREFIX)
    return app


flask_app = create_flask_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", "-i", dest="host", default=str(HOST), help="bind host")
    parser.add_argument("--port", "-p", dest="port", default=str(PORT), help="bind port")
    args = parser.parse_args()

    flask_app.run(host=args.host, port=int(args.port), debug=False, use_reloader=False, threaded=True)
