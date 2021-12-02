import logging
import repository
import uuid as uid
from typing import List
from model.storage_info import StorageInfoModel
from entity.metric_table import MetricTableEntity

logger = logging.getLogger("application")


class MetricTableDao(repository.MySQLRepository):

    def find_by_id(self, table_id: str, connection=None) -> MetricTableEntity:
        sql = "SELECT * FROM metric_table WHERE table_id = %(table_id)s"
        params = {
            "table_id": table_id
        }
        datas = self.find(sql, params=params, connection=connection)
        return MetricTableEntity(**datas[0]) if datas and len(datas) > 0 else None

    def find_by_field_id(self, field_id: str, connection=None) -> MetricTableEntity:
        sql = "SELECT " \
              "metric_table.*" \
              " FROM metric_table_field, metric_table" \
              " WHERE metric_table_field.field_id = %(field_id)s" \
              " AND metric_table_field.table_id = metric_table.table_id"
        params = {
            "field_id": field_id
        }
        datas = self.find(sql, params=params, connection=connection)
        return MetricTableEntity(**datas[0]) if datas and len(datas) > 0 else None

    def find_table_id_and_storage_type_by_name_like(self, table_name: str = None, connection=None) -> List[dict]:
        sql = "SELECT " \
              "metric_table.table_id," \
              "metric_table.table_name," \
              "metric_table.table_alias," \
              "metric_table.is_disabled," \
              "storage_info.storage_id," \
              "storage_info.storage_type" \
              " FROM metric_table,storage_metric_table,storage_info" \
              " WHERE metric_table.table_id = storage_metric_table.table_id" \
              " AND storage_metric_table.storage_id = storage_info.storage_id"
        params = dict()
        if table_name and len(table_name) > 0:
            sql += " AND metric_table.table_name like %(table_name)s"
            params.setdefault("table_name", "%{}%".format(table_name))
        sql += " ORDER BY metric_table.table_name ASC"
        return self.find(sql, params=params, connection=connection)

    def insert_metric_table(self, Storage_info_object: StorageInfoModel, metricItem: object, connection=None):
        if metricItem.id == None:
            table_id = str(uid.uuid4())
            metricItem.id = table_id
        else:
            table_id = str(metricItem.id)
        metricItem.table_type = Storage_info_object.table_type_code
        metricItem.table_format = Storage_info_object.table_type_format
        sql = "INSERT INTO metric_table \
                value (%(table_id)s\
                ,%(table_name)s\
                ,%(table_alias)s\
                ,%(table_type)s\
                ,%(table_format)s\
                ,%(table_description)s\
                ,%(is_disabled)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "table_id": table_id,
            "table_name": metricItem.name,
            "table_alias": metricItem.alias_name,
            "table_type": metricItem.table_type,
            "table_format": metricItem.table_format,
            "table_description": metricItem.description,
            "is_disabled": metricItem.get_status_disabled_type(),
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name,
        }
        self.excute_sql(sql, params=params, connection=connection)
