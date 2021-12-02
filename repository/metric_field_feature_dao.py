# -*- coding: utf-8 -*-
import logging
import repository
from model.storage_info import StorageInfoModel

logger = logging.getLogger("application")


class MetricFieldFeatureDao(repository.MySQLRepository):
    """ 維度欄位與特徵關聯 """

    def insert_metric_field_feature(self, feature_id: str, field_id: str, Storage_info_object: StorageInfoModel, connection):
        sql = "INSERT INTO metric_field_feature \
                value (%(field_id)s\
                ,%(feature_id)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "field_id": field_id,
            "feature_id": feature_id,
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)
