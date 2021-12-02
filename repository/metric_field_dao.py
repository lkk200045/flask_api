# -*- coding: utf-8 -*-
import logging
import repository
from typing import List, Tuple
from eyesmediapyutils.page import Paging
from entity.metric_field import MetricFieldEntity
from model.storage_info import StorageInfoModel

logger = logging.getLogger("application")


class MetricFieldDao(repository.MySQLRepository):

    def __generate_search_sql(
            self, field_names: List[str] = None,
            account_names: List[str] = None,
            storage_types: List[str] = None,
            table_types: List[str] = None,
            is_disabled: int = None,
            offset: int = None,
            limit: int = None,
            is_counting: bool = False
    ) -> Tuple[str, dict]:
        """
        建立搜尋SQL

        Args:
            field_names: 欄位存儲名稱或顯示名稱關鍵字
            account_names: 企業名稱關鍵字
            storage_types: 數據源類型
            table_types: 維度表類型
            is_disabled: 欄位狀態
            is_counting: 是否為筆數統計

        Returns:
            SQL語法, 查詢條件數值
        """
        # 維度欄位
        field_sql = "SELECT metric_field.* FROM metric_field WHERE 1=1"
        params = dict()
        if field_names and len(field_names) > 0:
            field_sql += " AND ("
            for idx, field_name in enumerate(field_names):
                key = "field_name" + str(idx)
                field_sql += "metric_field.field_name like %({})s".format(key)
                field_sql += " OR metric_field.field_alias like %({})s".format(key)
                params.setdefault(key, "%{}%".format(field_name))
                if idx + 1 < len(field_names):
                    field_sql += " OR "
            field_sql += ")"
        if is_disabled is not None and -1 < is_disabled < 2:
            field_sql += " AND metric_field.is_disabled = %(is_disabled)s"
            params.setdefault("is_disabled", is_disabled)

        # 其他關聯 SQL
        inner_join = False
        join_sql = "SELECT " \
                   "metric_table_field.field_id," \
                   "metric_table_field.table_id," \
                   "metric_table_field.storage_id," \
                   "metric_table.table_name," \
                   "metric_table.table_alias," \
                   "metric_table.table_type," \
                   "metric_table.is_disabled as table_is_disabled," \
                   "storage_info.storage_name," \
                   "storage_info.storage_alias," \
                   "storage_info.storage_type," \
                   "storage_info.is_disabled as storage_is_disabled," \
                   "provider_account.account_id," \
                   "provider_account.account_name" \
                   " FROM " \
                   "metric_table_field," \
                   "metric_table," \
                   "storage_info," \
                   "storage_provider," \
                   "provider_account" \
                   " WHERE 1=1"
        if table_types and len(table_types) > 0:
            join_sql += " AND metric_table.table_type in %(table_types)s"
            params.setdefault("table_types", table_types)
            inner_join = True
        if storage_types and len(storage_types) > 0:
            join_sql += " AND storage_info.storage_type in %(storage_types)s"
            params.setdefault("storage_types", storage_types)
            inner_join = True
        if account_names and len(account_names) > 0:
            join_sql += " AND ("
            for idx, account_name in enumerate(account_names):
                key = "account_name" + str(idx)
                join_sql += "provider_account.account_name like %({})s".format(key)
                params.setdefault(key, "%{}%".format(account_name))
                if idx + 1 < len(account_names):
                    join_sql += " OR "
            join_sql += ")"
            inner_join = True
        join_sql += " AND metric_table_field.table_id = metric_table.table_id" \
                    " AND metric_table_field.storage_id = storage_info.storage_id" \
                    " AND metric_table_field.storage_id = storage_provider.storage_id" \
                    " AND storage_provider.account_id = provider_account.account_id"
        # SQL 拼接
        sql = "SELECT " \
              "metric_field.*," \
              "tb01.table_id," \
              "tb01.storage_id," \
              "tb01.table_name," \
              "tb01.table_alias," \
              "tb01.table_type," \
              "tb01.table_is_disabled," \
              "tb01.storage_name," \
              "tb01.storage_alias," \
              "tb01.storage_type," \
              "tb01.storage_is_disabled," \
              "tb01.account_id," \
              "tb01.account_name" \
              " FROM (" + field_sql + ") as metric_field"
        if inner_join:
            sql += " INNER JOIN "
        else:
            sql += " LEFT JOIN "
        sql += "(" + join_sql + ") as tb01 on metric_field.field_id = tb01.field_id"
        # 如果是筆數統計則不須進行 join，直接回傳
        if is_counting:
            return sql, params
        # 排序
        sql += " ORDER BY metric_field.field_name"
        # 設定分頁 SQL
        if limit is not None:
            sql += " limit %(limit)s"
            params.setdefault("limit", limit)
        if offset is not None:
            sql += " offset %(offset)s"
            params.setdefault("offset", offset)
        # 拼接分類與特徵標籤統計
        catalog_sum_sql = "select field_id,count(catalog_tag_id) as cnt from metric_field_catalog group by field_id"
        feature_sum_sql = "select field_id,count(feature_id) as cnt from metric_field_feature group by field_id"
        sql = "SELECT " \
              "mfield.*," \
              "ifnull(metric_field_catalog.cnt,0) as catalog_counts," \
              "ifnull(metric_field_feature.cnt,0) as feature_counts" \
              " FROM (" + sql + ") as mfield"
        sql += " LEFT JOIN (" + catalog_sum_sql + ") as metric_field_catalog on mfield.field_id = metric_field_catalog.field_id" \
               + " LEFT JOIN (" + feature_sum_sql + ") as metric_field_feature on mfield.field_id = metric_field_feature.field_id"

        return sql, params

    def get_search_counts(
            self, field_names: List[str] = None,
            account_names: List[str] = None,
            storage_types: List[str] = None,
            table_types: List[str] = None,
            is_disabled: int = None,
            connection=None
    ) -> int:
        sql, params = self.__generate_search_sql(
            field_names=field_names,
            account_names=account_names,
            storage_types=storage_types,
            table_types=table_types,
            is_disabled=is_disabled,
            is_counting=True
        )
        return self.count(sql, params=params, connection=connection)

    def find_with_paging(
            self, paging: Paging,
            field_names: List[str] = None,
            account_names: List[str] = None,
            storage_types: List[str] = None,
            table_types: List[str] = None,
            is_disabled: int = None,
            connection=None
    ) -> List[dict]:
        sql, params = self.__generate_search_sql(
            field_names=field_names,
            account_names=account_names,
            storage_types=storage_types,
            table_types=table_types,
            is_disabled=is_disabled,
            offset=paging.start, limit=paging.limit
        )
        return self.find(sql, params=params, connection=connection)

    def find_by_id(self, field_id: str, connection=None) -> MetricFieldEntity:
        sql = "SELECT * FROM metric_field WHERE field_id = %(field_id)s"
        params = {
            "field_id": field_id
        }
        datas = self.find(sql, params=params, connection=connection)
        return MetricFieldEntity(**datas[0]) if datas and len(datas) > 0 else None

    def find_storage_table_by_id(self, field_id: str, connection=None) -> dict:
        sql = "SELECT " \
              "metric_field.*" \
              ",provider_account.account_id,provider_account.account_name" \
              " FROM " \
              "(" \
              "SELECT " \
              "metric_field.*," \
              "metric_table_field.storage_id," \
              "metric_table.table_id," \
              "metric_table.table_name," \
              "metric_table.table_alias," \
              "metric_table.table_type," \
              "metric_table.table_format," \
              "metric_table.table_description," \
              "metric_table.is_disabled as table_is_disabled," \
              "storage_info.storage_type," \
              "storage_info.storage_name," \
              "storage_info.storage_alias," \
              "storage_info.is_disabled as storage_is_disabled" \
              " FROM " \
              "metric_field,metric_table_field, metric_table,storage_info" \
              " WHERE " \
              "metric_field.field_id = %(field_id)s" \
              " AND metric_field.field_id = metric_table_field.field_id" \
              " AND metric_table_field.table_id = metric_table.table_id" \
              " AND metric_table_field.storage_id = storage_info.storage_id" \
              ") as metric_field" \
              " LEFT JOIN " \
              "(" \
              "SELECT storage_provider.storage_id, provider_account.account_id, provider_account.account_name" \
              " FROM storage_provider, provider_account" \
              " WHERE storage_provider.account_id = provider_account.account_id" \
              ") as provider_account ON metric_field.storage_id = provider_account.storage_id"
        params = {
            "field_id": field_id
        }
        datas = self.find(sql, params=params, connection=connection)
        return datas[0] if datas and len(datas) > 0 else None

    def count_by_name_and_table_id(self, field_name: str, table_id: str, connection=None) -> int:
        sql = "SELECT metric_table_field.field_id" \
              " FROM metric_field,metric_table_field" \
              " WHERE " \
              "metric_field.field_name = %(field_name)s" \
              " AND metric_table_field.table_id = %(table_id)s" \
              " AND metric_field.field_id = metric_table_field.field_id"
        params = {
            "field_name": field_name,
            "table_id": table_id
        }
        return self.count(sql, params=params, connection=connection)

    def insert_metric_field(self, Storage_info_object: StorageInfoModel, field_id: str, field_item: object, connection=None):
        sql = "INSERT INTO metric_field \
                value (%(field_id)s\
                ,%(field_name)s\
                ,%(field_alias)s\
                ,%(field_type)s\
                ,%(field_length)s\
                ,%(field_default_value)s\
                ,%(field_description)s\
                ,%(is_required)s\
                ,%(is_disabled)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "field_id": field_id,
            "field_name": field_item.name,
            "field_alias": field_item.alias_name,
            "field_type": field_item.field_type,
            "field_length": field_item.field_length,
            "field_default_value": field_item.field_default_value,
            "field_description": field_item.field_description,
            "is_required": field_item.get_status_required_type(),
            "is_disabled": field_item.get_status_disabled_type(),
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name,
        }
        self.excute_sql(sql, params=params, connection=connection)
