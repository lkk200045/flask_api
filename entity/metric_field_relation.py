# -*- coding: utf-8 -*-
from entity import SQLBaseEntityModel


class MetricFieldRelationEntity(SQLBaseEntityModel):
    """ 維度欄位關係表 """
    __db_tabel_name__ = "metric_field_relation"
    source_storage_id: str
    source_table_id: str
    source_field_id: str
    sink_storage_id: str
    sink_table_id: str
    sink_field_id: str
