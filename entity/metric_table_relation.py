# -*- coding: utf-8 -*-
from entity import SQLBaseEntityModel


class MetricTableRelationEntity(SQLBaseEntityModel):
    """ 維度表關係表 """
    __db_tabel_name__ = "metric_table_relation"
    source_storage_id: str
    source_table_id: str
    sink_storage_id: str
    sink_table_id: str
