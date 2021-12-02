# -*- coding: utf-8 -*-
import logging
import repository
import traceback
from typing import List
from model.storage_info import StorageInfoModel, StorageProviderMetricTablUpdateModel


class StorageMetricTableDao(repository.MySQLRepository):
    """ 數據源與維度表的關聯 """

    def find_storage_id_by_table_id(self, table_id: str, connection=None) -> List[str]:
        sql = "SELECT storage_id FROM storage_metric_table WHERE table_id = %(table_id)s"
        params = {
            "table_id": table_id
        }
        return [data["storage_id"] for data in self.find(sql, params=params, connection=connection)]

    def insert_storage_metric_table(self, Storage_info_object: StorageInfoModel, table_id: str, connection):
        sql = "INSERT INTO storage_metric_table \
                value (%(storage_id)s\
                ,%(table_id)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"
        params = {
            "storage_id": Storage_info_object.storage_id,
            "table_id": table_id,
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)

    def delete_metric_table_data(self, storage_id: str, table_id: str):
        sql = f''' delete from storage_metric_table WHERE storage_id= "{storage_id}" AND table_id = "{table_id}" '''
        try:
            connection = self.mysql_client.open_connection()
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        except:
            connection.rollback()
            logging.error(traceback.format_exc())
            raise
        finally:
            self.mysql_client.close_connection(connection)
        return storage_id

    def update_storage_metric_table(self, storage_id: str, table_id: str, user_name: str, user_id: str):
        storage_item = StorageProviderMetricTablUpdateModel()
        storage_item.storage_id = storage_id
        storage_item.user_id = user_id
        storage_item.user_name = user_name
        try:
            connection = self.mysql_client.open_connection()
            self.insert_storage_metric_table(storage_item, table_id, connection)
            connection.commit()
        except:
            connection.rollback()
            logging.error(traceback.format_exc())
            raise
        finally:
            self.mysql_client.close_connection(connection)
        return storage_id
