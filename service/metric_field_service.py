# -*- coding: utf-8 -*-
import logging
import traceback
import uuid as uid
from config.application import ApplicationContext
from model.enums import StorageType
from model.storage_info import StorageInfoModel
from repository.feature_handle_dao import FeatureHandleDao, FeatureHandleDaoMongo
from repository.metric_feature_dao import MetricFeatureDao
from repository.metric_field_feature_dao import MetricFieldFeatureDao
from repository.metric_field_dao import MetricFieldDao
from service.feature_handle_service import FeatureHandleService


class MetricFieldService(object):

    def __init__(self, app_context: ApplicationContext):
        self.__feature_handle_service = FeatureHandleService(app_context)
        self.__metric_field_feature_service = MetricFieldFeatureDao(app_context.mysql_client)
        self.__metric_field_dao = MetricFieldDao(app_context.mysql_client)
        self.__metric_feature_dao = MetricFeatureDao(app_context.mysql_client)
        self.__feature_handle_dao = FeatureHandleDao(app_context.mysql_client)

    def insert_metric_field(self, Storage_info_object: StorageInfoModel, connection):
        if Storage_info_object.storage_type == StorageType.STORAGE_TYPE_MONGODB.value:
            provider = self.__feature_handle_service.connect_config_mongoDB(Storage_info_object.connect_info, Storage_info_object.storage_name)
            self.__feature_handle_dao_mongo = FeatureHandleDaoMongo(provider)
        elif Storage_info_object.storage_type == StorageType.STORAGE_TYPE_MYSQL.value:
            provider = self.__feature_handle_service.init_other_mysql(Storage_info_object.connect_info, Storage_info_object.storage_name)
            connection_feature = provider.open_connection()

        for Storage_info in Storage_info_object.data:
            for field in Storage_info.fields:
                if field.id == None:
                    field_id = str(uid.uuid4())
                    field.id = field_id
                else:
                    field_id = str(Storage_info.id)
                # insert into metric_field
                try:
                    self.__metric_field_dao.insert_metric_field(Storage_info_object, field_id, field, connection)
                except:
                    logging.error(traceback.format_exc())
                    raise

                # 多標籤處理
                if field.feature_count > 0:
                    if Storage_info_object.storage_type == StorageType.STORAGE_TYPE_MYSQL.value:
                        try:
                            feature_list = self.__feature_handle_dao.feature_search(Storage_info.name, field.name, connection_feature)
                        except:
                            logging.error(traceback.format_exc())
                            raise
                    elif Storage_info_object.storage_type == StorageType.STORAGE_TYPE_MONGODB.value:
                        try:
                            self.__feature_handle_dao_mongo._set_collection(Storage_info.name)
                            feature_list = self.__feature_handle_dao_mongo.feature_search_mongo(field.name)
                        except:
                            connection_feature.close()
                            logging.error(traceback.format_exc())
                            raise

                    if feature_list != None:
                        # insert into metric_feature
                        try:
                            feature_id_list = []
                            for feature in feature_list:
                                feature_label = list(feature.keys())[0],
                                feature_value = list(feature.values())[0],
                                feature_id = self.__metric_feature_dao.insert_metric_feature(
                                    Storage_info_object.user_id,
                                    Storage_info_object.user_name,
                                    feature_label, feature_value, connection)
                                feature_id_list.append(feature_id)
                        except:
                            logging.error(traceback.format_exc())
                            raise

                        # insert into metric_field_feature
                        try:
                            for feature_id in feature_id_list:
                                self.__metric_field_feature_service.insert_metric_field_feature(
                                    feature_id, field_id, Storage_info_object,
                                    connection)
                        except:
                            logging.error(traceback.format_exc())
                            raise

        if Storage_info_object.storage_type == StorageType.STORAGE_TYPE_MYSQL.value:
            connection_feature.close()
