# -*- coding: utf-8 -*-
import logging
import flask_pydantic
from flask import Blueprint
from flask import current_app
from flask import json
from service.field_service import FieldService
from model.metric_field import MetricFieldSearchReqModel
from model.metric_field import MetricFieldNewReqModel

logger = logging.getLogger("application")

field_api = Blueprint("field_api", __name__)


@field_api.post("/field/new")
@flask_pydantic.validate()
def add_field(body: MetricFieldNewReqModel):
    """ 新增維度欄位 """
    app_context = current_app.config["app_context"]
    field_service = FieldService(app_context)
    return json.jsonify(field_service.insert_field_with_payload(req_model=body))


@field_api.post("/field/search")
@flask_pydantic.validate()
def search_field(body: MetricFieldSearchReqModel):
    """ 搜尋 """
    app_context = current_app.config["app_context"]
    field_service = FieldService(app_context)
    return json.jsonify(field_service.search_field_with_payload(req_model=body))


@field_api.get("/field/<string:field_id>")
def get_field(field_id: str):
    """ 查詢維度欄位明細 """
    app_context = current_app.config["app_context"]
    field_service = FieldService(app_context)
    return json.jsonify(field_service.get_field_with_payload(field_id))
