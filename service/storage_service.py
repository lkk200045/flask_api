import json
import traceback
import logging
import uuid as uid
import hashlib
from eyesmediapyutils.page import Paging
from eyesmediapyutils.datetime import DateTimeUtils
from eyesmediapyutils.validator import create_md5
from model.connectInfo import connectInfoResModal
from model.enums import UpdateType
from eyesmediapyutils.exceptions import CommonRuntimeException
from model.storage_info import StorageInfoModel, StorageInfoUpdateModel, StorageProviderMetricTablUpdateModel, StorageSearchReqModal, StorageSearchListResModal, StorageSearchResModal
from repository.storage_info_dao import StorageDao
from repository.storage_provider_dao import StorageProviderDao
from repository.metric_table_dao import MetricTableDao
from config.application import ApplicationContext
from service.metric_field_service import MetricFieldService
from repository.storage_metric_table_dao import StorageMetricTableDao
from repository.metric_table_field_dao import MetricTableFieldDao
from repository.metric_field_catalog_dao import MetricFieldCatalogDao
from repository.system_dao import SystemParamsConfigDao
from flask import current_app



#搜尋數據來源
class StorageSearchServiceList(object):
    def __init__(self, app_context: ApplicationContext):
         self.search_storage_info_dao = StorageDao(app_context.mysql_client)
         self.__dt_utils = DateTimeUtils(app_context.timezone)

    def split_storage_name(storage_names):
        storage_names = str(storage_names).split(" ")
        result = []
        for storage_name in storage_names:
            result.append(storage_name)
        return result

    def search_storage(self, req_model: StorageSearchReqModal):
        search_fields = list()
        try:
            data_count = self.search_storage_info_dao.get_counts(req_model)

            paging = Paging(page_no=req_model.page_no, limit=req_model.page_size,data_count=data_count)
            
            storage_fields = self.search_storage_info_dao.find_with_paging(paging,req_model)

            for storage_name in storage_fields:
                storage = StorageSearchListResModal(**storage_name)
                storage.mdy_date = self.__dt_utils.utc_to_localize(storage.mdy_date)
                search_fields.append(json.loads(storage.json(by_alias=True)))
        except:
            logging.error(traceback.format_exc())
            raise
        return search_fields,paging

class StorageSearchService(object):
    def __init__(self, app_context: ApplicationContext):
         self.search_storage_info_dao = StorageDao(app_context.mysql_client)
         self.__dt_utils = DateTimeUtils(app_context.timezone)
    def search_storage(self, storage_id: str):
        storage_field = list()
        connect_info = dict()
        account_list = list()
        structure_list = list()
        try:
            storage_fields = self.search_storage_info_dao.search_storage_info(storage_id)
            
            connect_info['account'] = storage_fields[0]['storage_account']
            connect_info['pwd'] = storage_fields[0]['storage_pwd']
            connect_info['host'] = storage_fields[0]['storage_host']
            connect_info['port'] = storage_fields[0]['storage_port']
            connect_info['url'] = storage_fields[0]['storage_url']
            
            account = dict()
            structure = dict()
            for storage_name in storage_fields:

                account['accountId'] = storage_name['account_id']
                account['accountName'] = storage_name['account_name']
                account_list.append(account)
                structure['tableId'] = storage_name['table_id']
                structure['tableName'] = storage_name['table_name']
                structure['tableAlias'] = storage_name['table_alias']
                structure['isDisabled'] = storage_name['is_disabled']
                structure['storageType'] = storage_name['storage_type']
                structure_list.append(structure)
            
            storage = StorageSearchResModal(**storage_fields[0], connect_info=connectInfoResModal(**connect_info), 
                                                                                                    account=account_list, 
                                                                                                    structure =structure_list)
            storage.mdy_date = self.__dt_utils.utc_to_localize(storage.mdy_date)

            storage_field.append(json.loads(storage.json(by_alias=True)))
        except:
            logging.error(traceback.format_exc())
            raise
        return storage_field

class StorageInsertUpdateCheckService(object):
    """ 數據來源檢查 """

    def __init__(self, app_context: ApplicationContext):
        self.insert_check_dao = StorageDao(app_context.mysql_client)

    def insert_check(self, storage_type: str, storage_name: str):
        has_exist = self.insert_check_dao.insert_check(storage_type, storage_name)
        return has_exist


class StorageInsertService(object):
    """ 數據來源新增 """

    def __init__(self, app_context: ApplicationContext):
        self.__insert_storeage_dao = StorageDao(app_context.mysql_client)
        self.__insert_storeage_provider_dao = StorageProviderDao(app_context.mysql_client)
        self.__insert_metric_table_dao = MetricTableDao(app_context.mysql_client)
        self.__insert_storage_metric_table_dao = StorageMetricTableDao(app_context.mysql_client)
        self.__insert_metric_field_dao = MetricTableFieldDao(app_context.mysql_client)
        self.__insert_metric_field_catalog_dao = MetricFieldCatalogDao(app_context.mysql_client)
        self.__insert_metric_field_service = MetricFieldService(app_context)
        self.__system_params_config_dao = SystemParamsConfigDao(app_context.mysql_client)
        self.__storage_check_service = StorageInsertUpdateCheckService(app_context)

    def find_config_code(self, Storage_info_object: StorageInfoModel):
        Storage_config = self.__system_params_config_dao.find_by_group_code(group_code="storage_type", config_codes=[Storage_info_object.storage_type])
        Storage_info_object.storage_type_code = Storage_config[0].config_code
        data = "storage_type" + str(Storage_config[0].config_code)
        child_key = create_md5(data)
        table_format = self.__system_params_config_dao.find_config_child_table(child_key, "table_format")
        Storage_info_object.table_type_format = table_format[0].config_code
        table_type_code = self.__system_params_config_dao.find_config_child_table(child_key, "table_type")
        Storage_info_object.table_type_code = table_type_code[0].config_code

    def insert_storage_data_service(self, Storage_info_object: StorageInfoModel):
        storageId = str(uid.uuid4())
        Storage_info_object.storage_id = storageId
        has_exist = self.__storage_check_service.insert_check(Storage_info_object.storage_type, Storage_info_object.storage_name)
        if list(has_exist[0].values())[0] > 0:
            raise CommonRuntimeException("519800003")
        self.find_config_code(Storage_info_object)

        connection = self.__insert_storeage_dao.open_connection()
        try:
            # insert into storage_info
            self.__insert_storeage_dao.insert_storage(Storage_info_object, connection)

            # insert into storage_provider
            for id in Storage_info_object.account_id:
                self.__insert_storeage_provider_dao.insert_storage_provider(Storage_info_object, id, connection)

            # #insert into metric_field
            self.__insert_metric_field_service.insert_metric_field(Storage_info_object, connection)

            for Storage_info in Storage_info_object.data:
                # insert into metric_table
                self.__insert_metric_table_dao.insert_metric_table(
                    Storage_info_object, Storage_info, connection)

                # insert into storage_metric_table
                self.__insert_storage_metric_table_dao.insert_storage_metric_table(
                    Storage_info_object, Storage_info.id, connection)
                for field in Storage_info.fields:
                    # #insert into metric_table_field
                    table_id = Storage_info.id
                    field_id = field.id
                    self.__insert_metric_field_dao.insert_metric_table_field(
                        Storage_info_object, table_id, field_id, connection)
                    # #insert into metric_table_field
                    for catalog_tag_id in field.catalog_tag_id:
                        field_id = field.id
                        catalog_tag_id = catalog_tag_id
                        self.__insert_metric_field_catalog_dao.insert_metric_table_field(
                            Storage_info_object, field_id, catalog_tag_id,
                            connection)

            connection.commit()
            return storageId
        except:
            self.__insert_storeage_dao.rollback_connection(connection)
            logging.error(traceback.format_exc())
            raise
        finally:
            self.__insert_storeage_dao.close_connection(connection)


class StorageUpdateService(object):
    """ 數據來源編輯 """

    def __init__(self, app_context: ApplicationContext):
        self.__storage_dao = StorageDao(app_context.mysql_client)
        self.__storage_provider_dao = StorageProviderDao(app_context.mysql_client)
        self.__storage_metric_table_dao = StorageMetricTableDao(app_context.mysql_client)

    def update_storage_info(self, data: StorageInfoUpdateModel):
        return self.__storage_dao.update_storage_info_data(data.storage_id, data.update_column_name, data.value)

    def update_storage_provider_metric(self, data: StorageProviderMetricTablUpdateModel):
        if data.update_table == UpdateType.UPDATE_TYPE_ACCOUNT.value:
            return self.__storage_provider_dao.update_storage_provider_data(data.storage_id, data.update_value, data.user_name, data.user_id)
        if data.update_table == UpdateType.UPDATE_TYPE_TABLE.value:
            return self.__storage_metric_table_dao.update_storage_metric_table(data.storage_id, data.update_value, data.user_name, data.user_id)
        raise CommonRuntimeException("999900001")

    def delete_storage_provider_metric(self, data: StorageProviderMetricTablUpdateModel):
        if data.update_table == UpdateType.UPDATE_TYPE_ACCOUNT.value:
            return self.__storage_provider_dao.delete_storage_provider_data(data.storage_id, data.update_value)
        if data.update_table == UpdateType.UPDATE_TYPE_TABLE.value:
            return self.__storage_metric_table_dao.delete_metric_table_data(data.storage_id, data.update_value)
        raise CommonRuntimeException("999900001")
