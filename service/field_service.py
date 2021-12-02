# -*- coding: utf-8 -*-
import logging
import traceback
import time
import json
import uuid
from eyesmediapyutils.page import Paging
from eyesmediapyutils.payload import ReponsePayloadBulider
from eyesmediapyutils.exceptions import CommonRuntimeException
from eyesmediapyutils.datetime import DateTimeUtils
from config.application import ApplicationContext
from repository.metric_field_dao import MetricFieldDao
from repository.metric_table_dao import MetricTableDao
from repository.metric_feature_dao import MetricFeatureDao
from repository.metric_catalog_tag_dao import MetricCatalogTagDao
from repository.metric_table_field_dao import MetricTableFieldDao
from repository.system_dao import SystemParamsConfigDao
from model.enums import StatusType
from model.metric_field import MetricFieldModel
from model.metric_field import MetricFieldTableModel
from model.metric_field import MetricFieldFeatureModel
from model.metric_field import MetricCatalogTagModel
from model.metric_field import MetricFieldSearchReqModel
from model.metric_field import MetricFieldSearchResModel
from model.metric_field import MetricFieldSearchSummaryResModel
from model.metric_field import MetricFieldNewReqModel
from entity.metric_field import MetricFieldEntity
from entity.metric_feature import MetricFeatureEntity
from entity.metric_field_catalog import MetricFieldCatalogEntity
from entity.metric_field_feature import MetricFieldFeatureEntity
from entity.metric_feature_catalog import MetricFeatureCatalogEntity

logger = logging.getLogger("application")


class FieldService(object):

    def __init__(self, app_context: ApplicationContext):
        self.__messages = app_context.messages
        self.__dt_utils = DateTimeUtils(app_context.timezone)
        self.__metric_field_dao = MetricFieldDao(app_context.mysql_client)
        self.__metric_table_dao = MetricTableDao(app_context.mysql_client)
        self.__metric_feature_dao = MetricFeatureDao(app_context.mysql_client)
        self.__metric_catalog_tag_dao = MetricCatalogTagDao(app_context.mysql_client)
        self.__metric_table_field_dao = MetricTableFieldDao(app_context.mysql_client)
        self.__system_params_config_dao = SystemParamsConfigDao(app_context.mysql_client)

    def insert_field_with_payload(self, req_model: MetricFieldNewReqModel) -> dict:
        payload = ReponsePayloadBulider(self.__messages)
        try:
            sstime = time.time()
            field_id = self.insert_field(req_model)
            costtime = time.time() - sstime
            resp_json = payload.bulid("996600001", data=field_id, cost_time=costtime)
            return resp_json
        except CommonRuntimeException as crex:
            logger.error("request:{}, error:{}".format(req_model, crex.code))
            return payload.bulid_from_exception(crex)
        except:
            logger.error("request:{}\n{}".format(req_model, traceback.format_exc()))
            return payload.bulid("999999999")

    def insert_field(self, req_model: MetricFieldNewReqModel) -> str:
        table_id = req_model.table_id
        tag_id = req_model.tag_id
        has_tag_id = tag_id is not None and len(tag_id) > 0
        # 驗證必填參數
        if not self.__metric_table_dao.find_by_id(table_id=table_id):
            raise CommonRuntimeException("519800004", table_id)
        # 驗證資料是否重複
        if self.__metric_field_dao.count_by_name_and_table_id(req_model.field_name, table_id) > 0:
            raise CommonRuntimeException("519800002", req_model.field_name)
        # 驗證選填參數
        if has_tag_id and not self.__metric_catalog_tag_dao.find_by_id(tag_id=tag_id):
            raise CommonRuntimeException("519800004", tag_id)
        # 執行新增
        connection = None
        try:
            connection = self.__metric_field_dao.open_connection()

            # 新增欄位
            field_entity = MetricFieldEntity.parse_obj(req_model)
            self.__metric_field_dao.insert(db_entity=field_entity, connection=connection)
            field_id = field_entity.field_id
            # 建立欄位與表關聯
            self.__metric_table_field_dao.insert_from_select_by_table_id(table_id=table_id, field_id=str(field_id), connection=connection)
            # 建立欄位與分類關聯
            if has_tag_id:
                self.__metric_field_dao.insert(db_entity=MetricFieldCatalogEntity(field_id=field_id, catalog_tag_id=uuid.UUID(tag_id)), connection=connection)

            # 新增特徵標籤
            feature_entities = list()
            field_feature_entities = list()  # 欄位與特徵關聯
            feature_catalog_entities = list()  # 特徵與分類關聯
            if req_model.has_features():
                for featrue in req_model.features:
                    feature_entity = MetricFeatureEntity(feature_label=featrue.feature_label, feature_value=featrue.feature_value)
                    feature_entities.append(feature_entity)
                    field_feature_entities.append(MetricFieldFeatureEntity(field_id=field_id, feature_id=feature_entity.feature_id))
                    if has_tag_id:
                        feature_catalog_entities.append(MetricFeatureCatalogEntity(feature_id=feature_entity.feature_id, catalog_tag_id=uuid.UUID(tag_id)))
            self.__metric_field_dao.insert_many(db_entities=feature_entities, connection=connection)
            # 建立欄位與特徵關聯
            self.__metric_field_dao.insert_many(db_entities=field_feature_entities, connection=connection)
            # 建立特徵與分類關聯
            if feature_catalog_entities and len(feature_catalog_entities) > 0:
                self.__metric_field_dao.insert_many(db_entities=feature_catalog_entities, connection=connection)

            connection.commit()
            return str(field_id)
        except:
            self.__metric_field_dao.rollback_connection(connection)
            raise
        finally:
            self.__metric_field_dao.close_connection(connection)

    def search_field_with_payload(self, req_model: MetricFieldSearchReqModel) -> dict:
        payload = ReponsePayloadBulider(self.__messages)
        try:
            sstime = time.time()

            data_count = self.__metric_field_dao.get_search_counts(
                field_names=req_model.get_field_names(),
                account_names=req_model.get_account_names(),
                storage_types=req_model.storage_type_code,
                table_types=req_model.table_type_code,
                is_disabled=req_model.get_status_type()
            )
            paging = Paging(page_no=req_model.page_no, limit=req_model.limit, data_count=data_count)

            metric_fields = self.__metric_field_dao.find_with_paging(
                field_names=req_model.get_field_names(),
                account_names=req_model.get_account_names(),
                storage_types=req_model.storage_type_code,
                table_types=req_model.table_type_code,
                is_disabled=req_model.get_status_type(),
                paging=paging
            )

            storage_type_name_mapping = self.__get_storage_type_name_mapping(metric_fields)
            search_fields = list()
            for metric_field in metric_fields:
                # 關聯資料 response
                table = MetricFieldTableModel(**metric_field)
                table.storage_type = storage_type_name_mapping.get(table.storage_type)
                table.is_disabled = metric_field.get("table_is_disabled") == StatusType.DISABLE.value
                # 維度欄位 response
                field = MetricFieldSearchResModel(**metric_field,
                                                  table=table,
                                                  summary=MetricFieldSearchSummaryResModel(**metric_field))
                if not field.mdy_user_id:
                    field.mdy_user_id = metric_field["crt_user_id"]
                if not field.mdy_user_name:
                    field.mdy_user_id = metric_field["crt_user_name"]
                if not field.mdy_date:
                    field.mdy_date = self.__dt_utils.utc_to_localize(metric_field["crt_date"])
                else:
                    field.mdy_date = self.__dt_utils.utc_to_localize(field.mdy_date)
                search_fields.append(json.loads(field.json(by_alias=True)))

            costtime = time.time() - sstime
            resp_json = payload.bulid("996600001", data=search_fields, cost_time=costtime, paging=paging)
            return resp_json
        except CommonRuntimeException as crex:
            logger.error("request:{}, error:{}".format(req_model, crex.code))
            return payload.bulid_from_exception(crex)
        except:
            logger.error("request:{}\n{}".format(req_model, traceback.format_exc()))
            return payload.bulid("999999999")

    def __get_storage_type_name_mapping(self, metric_fields) -> dict:
        codes = list()
        for metric_field in metric_fields:
            storage_type = metric_field.get("storage_type")
            if storage_type and storage_type not in codes:
                codes.append(storage_type)
        name_mapping = dict()
        if codes and len(codes) > 0:
            configs = self.__system_params_config_dao.find_by_group_code(group_code="storage_type",
                                                                         config_codes=codes,
                                                                         is_disabled=StatusType.ENABLE.value
                                                                         )
            for config in configs:
                name_mapping.setdefault(config.config_code, config.config_name)
        return name_mapping

    def get_field_with_payload(self, field_id: str) -> dict:
        payload = ReponsePayloadBulider(self.__messages)
        try:
            sstime = time.time()
            field = self.get_field(field_id)
            costtime = time.time() - sstime
            return payload.bulid("996600001", data=json.loads(field.json(by_alias=True)), cost_time=costtime)
        except CommonRuntimeException as crex:
            logger.error("request:{}, error:{}".format(field_id, crex.code))
            return payload.bulid_from_exception(crex)
        except:
            logger.error("request:{}\n{}".format(field_id, traceback.format_exc()))
            return payload.bulid("999999999")

    def get_field(self, field_id: str) -> MetricFieldModel:
        metric_field = self.__metric_field_dao.find_storage_table_by_id(field_id)
        if not metric_field:
            raise CommonRuntimeException("519800004", field_id)
        field = MetricFieldModel(**metric_field)
        # 維度表與數據源
        table = MetricFieldTableModel(**metric_field)
        table.is_disabled = metric_field.get("table_is_disabled") == StatusType.DISABLE.value
        field.table = table
        # 抓取分類
        catalog_tag_entity = self.__metric_catalog_tag_dao.find_by_field_id(field_id)
        if catalog_tag_entity:
            field.catalog = MetricCatalogTagModel.from_orm(catalog_tag_entity)
        # 抓取特徵
        feature_entities = self.__metric_feature_dao.find_by_field_id(field_id)
        if feature_entities and len(feature_entities) > 0:
            field.features = [MetricFieldFeatureModel.from_orm(entity) for entity in feature_entities]
        # change UTC to local datetime
        field.mdy_date = self.__dt_utils.utc_to_localize(field.mdy_date)
        return field
