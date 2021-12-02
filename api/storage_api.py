# -*- coding: utf-8 -*-
import flask_pydantic
import traceback
import logging
import time
from eyesmediapyutils.page import Paging
from eyesmediapyutils.exceptions import CommonRuntimeException
from datetime import datetime
from flask import Blueprint
from flask import json
from flask import current_app
from eyesmediapyutils.payload import ReponsePayloadBulider
from service.storage_service import StorageInsertService, StorageInsertUpdateCheckService, StorageSearchService, StorageSearchServiceList, StorageUpdateService
from model.storage_info import StorageInfoModel, StorageInfoUpdateModel, StorageProviderMetricTablUpdateModel, StorageSearchReqModal

logger = logging.getLogger("application")

storage_api = Blueprint("storage_api", __name__)


@storage_api.post("/storage/check")
@flask_pydantic.validate()
def insert_check(body: StorageInfoModel):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    try:
        sstime = time.time()
        Storage_insert_service = StorageInsertUpdateCheckService(app_context)
        storage_exit = Storage_insert_service.insert_check(body.storage_type, body.storage_name)
        storage_exit = list(storage_exit[0].values())[0]
        if storage_exit > 0:
            Desc = 1
        else:
            Desc = 0
        costtime = time.time() - sstime
        now = datetime.utcnow()
        resp_json = payload.bulid("996600001", data=Desc, message_datetime=now)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        logger.error(traceback.format_exc())
        return json.jsonify(payload.bulid("999999999"))


@storage_api.post("/storage/new")
@flask_pydantic.validate()
def storage_insert(body: StorageInfoModel):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    sstime = time.time()
    now = datetime.utcnow()
    try:
        Storage_insert_service = StorageInsertService(app_context)
        storage_id = Storage_insert_service.insert_storage_data_service(body)
        resp_json = payload.bulid("996600001", data=storage_id, message_datetime=now)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        logging.error(traceback.format_exc())
        return json.jsonify(payload.bulid("999999999"))


@storage_api.post('/storage/update')
@flask_pydantic.validate()
def storage_update(body: StorageInfoUpdateModel):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    sstime = time.time()
    now = datetime.utcnow()
    costtime = time.time() - sstime
    try:
        Storage_update_service = StorageUpdateService(app_context)
        storage_id = Storage_update_service.update_storage_info(body)
        resp_json = payload.bulid("996600001", data=storage_id, message_datetime=now)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        return json.jsonify(payload.bulid("999999999"))


@storage_api.patch('/storage/relation/<string:storage_id>/<string:update_table>/<string:update_value>')
@flask_pydantic.validate()
def storage_provider_metric_relation_insert(storage_id: str, update_table: str, update_value: str, body: StorageProviderMetricTablUpdateModel):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    now = datetime.utcnow()
    body.storage_id = storage_id
    body.update_table = update_table
    body.update_value = update_value
    try:
        Storage_update_service = StorageUpdateService(app_context)
        storage_id = Storage_update_service.update_storage_provider_metric(body)
        resp_json = payload.bulid("996600001", data=storage_id, message_datetime=now)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        return json.jsonify(payload.bulid("999999999"))


@storage_api.delete('/storage/relation/<string:storage_id>/<string:update_table>/<string:update_value>')
@flask_pydantic.validate()
def storage_provider_metric_relation_delete(storage_id: str, update_table: str, update_value: str, body: StorageProviderMetricTablUpdateModel):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    now = datetime.utcnow()
    body.storage_id = storage_id
    body.update_table = update_table
    body.update_value = update_value
    try:
        Storage_update_service = StorageUpdateService(app_context)
        storage_id = Storage_update_service.delete_storage_provider_metric(body)
        resp_json = payload.bulid("996600001",
                                  data=storage_id,
                                  message_datetime=now)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        return json.jsonify(payload.bulid("999999999"))

@storage_api.post('/storage/search')
@flask_pydantic.validate()
def storage_search_list(body: StorageSearchReqModal):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    now = datetime.utcnow()
    try:   
        Storage_search_service = StorageSearchServiceList(app_context)
        storage_items,paging = Storage_search_service.search_storage(body)
        resp_json = payload.bulid("996600001",
                                  data=storage_items,
                                  message_datetime=now,paging = paging)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        return json.jsonify(payload.bulid("999999999"))


@storage_api.get('/storage/search/<string:storage_id>')
@flask_pydantic.validate()
def storage_search(storage_id: str):
    app_context = current_app.config["app_context"]
    payload = ReponsePayloadBulider(app_context.messages)
    now = datetime.utcnow()
    try:   
        Storage_search_service = StorageSearchService(app_context)
        storage_items= Storage_search_service.search_storage(storage_id)
        resp_json = payload.bulid("996600001",
                                  data=storage_items,
                                  message_datetime=now)
        return json.jsonify(resp_json)
    except CommonRuntimeException as crex:
        logging.error(traceback.format_exc())
        return json.jsonify(payload.bulid_from_exception(crex))
    except:
        logging.error(traceback.format_exc())
        return json.jsonify(payload.bulid("999999999"))
