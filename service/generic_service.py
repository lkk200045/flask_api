# -*- coding: utf-8 -*-
import logging
import traceback
import time
import json
from typing import List
from eyesmediapyutils.payload import ReponsePayloadBulider
from eyesmediapyutils.exceptions import CommonRuntimeException
from eyesmediapyutils.validator import create_md5
from config.application import ApplicationContext
from repository.system_dao import SystemParamsConfigDao
from repository.metric_table_dao import MetricTableDao
from repository.provider_account_dao import ProviderAccountDao
from model.enums import GenericConstantGroupCode
from model.enums import StatusType
from model.generic_model import GenericConstantAutocompleteReqModel
from model.generic_model import GenericConstantAutocompleteResModel

logger = logging.getLogger("application")


class GenericConstantService(object):

    def __init__(self, app_context: ApplicationContext):
        self.__messages = app_context.messages
        self.__system_params_config_dao = SystemParamsConfigDao(app_context.mysql_client)
        self.__metric_table_dao = MetricTableDao(app_context.mysql_client)
        self.__provider_account_dao = ProviderAccountDao(app_context.mysql_client)

    def autocomplete_with_payload(self, group_code: str, req_model: GenericConstantAutocompleteReqModel) -> dict:
        payload = ReponsePayloadBulider(self.__messages)
        try:
            sstime = time.time()
            datas = self.autocomplete(group_code=group_code, text=req_model.text)
            costtime = time.time() - sstime
            resp_json = payload.bulid("996600001", data=datas, cost_time=costtime)
            return resp_json
        except CommonRuntimeException as crex:
            logger.error("request({}):{}, error:{}".format(group_code, req_model, crex.code))
            return payload.bulid_from_exception(crex)
        except:
            logger.error("request({}):{}\n{}".format(group_code, req_model, traceback.format_exc()))
            return payload.bulid("999999999")

    def autocomplete(self, group_code: str, text: str = None) -> List[dict]:
        if not GenericConstantGroupCode.has_value(group_code):
            raise CommonRuntimeException("519800001", group_code)
        config_group = GenericConstantGroupCode(group_code)
        datas = list()
        # 歸屬企業
        if config_group.is_biz_account():
            accounts = self.__provider_account_dao.find_account_id_by_name_like(account_name=text)
            for account in accounts:
                datas.append(json.loads(GenericConstantAutocompleteResModel(
                    id=account.account_id,
                    name=account.account_name
                ).json(by_alias=True)))
            return datas
        # 維度表
        if config_group.is_metric_table():
            metric_tables = self.__metric_table_dao.find_table_id_and_storage_type_by_name_like(table_name=text)
            for metric_table in metric_tables:
                datas.append(json.loads(GenericConstantAutocompleteResModel(
                    id=metric_table["table_id"],
                    name=metric_table["table_name"],
                    alias_name=metric_table["table_alias"],
                    storage_type=metric_table["storage_type"],
                    is_disabled=metric_table["is_disabled"]
                ).json(by_alias=True)))
            return datas
        # 系統常數
        sys_configs = self.__system_params_config_dao.find_by_group_code(group_code=config_group.value, is_disabled=StatusType.ENABLE.value)
        for config in sys_configs:
            datas.append(json.loads(GenericConstantAutocompleteResModel(
                id=config.config_code,
                name=config.config_name
            ).json(by_alias=True)))
        return datas

    def find_children_with_payload(self, group_code: str, config_code: str) -> dict:
        payload = ReponsePayloadBulider(self.__messages)
        try:
            sstime = time.time()
            datas = self.find_children(group_code=group_code, config_code=config_code)
            costtime = time.time() - sstime
            resp_json = payload.bulid("996600001", data=datas, cost_time=costtime)
            return resp_json
        except CommonRuntimeException as crex:
            logger.error("request({}):{}, error:{}".format(group_code, config_code, crex.code))
            return payload.bulid_from_exception(crex)
        except:
            logger.error("request({}):{}\n{}".format(group_code, config_code, traceback.format_exc()))
            return payload.bulid("999999999")

    def find_children(self, group_code: str, config_code: str) -> List[dict]:
        if not GenericConstantGroupCode.has_value(group_code):
            raise CommonRuntimeException("519800001", group_code)
        if not config_code or len(config_code) == 0:
            raise CommonRuntimeException("519800001", config_code)

        config_group = GenericConstantGroupCode(group_code)
        # 歸屬企業或維度表不支援連動式
        if config_group.is_biz_account() or config_group.is_metric_table():
            raise CommonRuntimeException("519800001", group_code)
        # 抓取子層系統常數資料
        config_parent_code = create_md5(config_group.value.lower() + config_code)
        sys_configs = self.__system_params_config_dao.find_by_parent_code(config_parent_code=config_parent_code,
                                                                          is_disabled=StatusType.ENABLE.value
                                                                          )
        datas = list()
        for config in sys_configs:
            datas.append(json.loads(GenericConstantAutocompleteResModel(
                id=config.config_code,
                name=config.config_name
            ).json(by_alias=True)))
        return datas
