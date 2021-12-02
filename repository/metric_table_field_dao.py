# -*- coding: utf-8 -*-
import logging
import repository
from entity import SystmeUser
from model.storage_info import StorageInfoModel

logger = logging.getLogger("application")


class MetricTableFieldDao(repository.MySQLRepository):
    """ 維度表與欄位關聯 """

    def insert_metric_table_field(self, Storage_info_object: StorageInfoModel, table_id: str, field_id: str, connection):
        sql = "INSERT INTO metric_table_field \
                value (%(storage_id)s\
                ,%(table_id)s\
                ,%(field_id)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "storage_id": Storage_info_object.storage_id,
            "table_id": table_id,
            "field_id": field_id,
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)

    def insert_from_select_by_table_id(self, table_id: str,
                                       field_id: str,
                                       user_id: str = SystmeUser.USER_ID.value,
                                       user_name: str = SystmeUser.USER_NAME.value,
                                       connection=None
                                       ):
        sql = "INSERT INTO metric_table_field (" \
              "storage_id, table_id, field_id, crt_user_id, crt_user_name, crt_date, mdy_user_id, mdy_user_name, mdy_date" \
              ")" \
              " SELECT " \
              "storage_id," \
              "table_id," \
              "%(field_id)s," \
              "%(user_id)s,%(user_name)s,now(),%(user_id)s,%(user_name)s,now()" \
              " FROM storage_metric_table" \
              " WHERE table_id = %(table_id)s"
        params = {
            "table_id": table_id,
            "field_id": field_id,
            "user_id": user_id,
            "user_name": user_name
        }
        self.excute_sql(sql=sql, params=params, connection=connection)
