# -*- coding: utf-8 -*-
import logging
import flask_pydantic
from flask import Blueprint
from flask import current_app
from flask import json
from model.generic_model import GenericConstantAutocompleteReqModel
from service.generic_service import GenericConstantService

logger = logging.getLogger("application")

generic_api = Blueprint("generic_api", __name__)


@generic_api.post("/generic/constant/<string:group_code>")
@flask_pydantic.validate()
def autocomplete(group_code: str, body: GenericConstantAutocompleteReqModel):
    """ 下拉式選單或 autocomplete 元件 """
    app_context = current_app.config["app_context"]
    generic_service = GenericConstantService(app_context)
    return json.jsonify(generic_service.autocomplete_with_payload(group_code, body))


@generic_api.get("/generic/constant/<string:group_code>/<string:config_code>/children")
@flask_pydantic.validate()
def find_children(group_code: str, config_code: str):
    """ 抓取子層資料 """
    app_context = current_app.config["app_context"]
    generic_service = GenericConstantService(app_context)
    return json.jsonify(generic_service.find_children_with_payload(group_code, config_code))
