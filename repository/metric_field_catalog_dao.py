# -*- coding: utf-8 -*-
import logging
import repository
from model.storage_info import StorageInfoModel

logger = logging.getLogger("application")


class MetricFieldCatalogDao(repository.MySQLRepository):
    """ 維度欄位與分類關聯 """

    def insert_metric_table_field(self, Storage_info_object: StorageInfoModel, field_id: str, catalog_tag_id: str, connection):
        sql = "INSERT INTO metric_field_catalog \
                value (%(field_id)s\
                ,%(catalog_tag_id)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "field_id": field_id,
            "catalog_tag_id": catalog_tag_id,
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)
