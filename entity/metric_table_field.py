# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricTableFieldEntity(SQLBaseEntityModel):
    """ 維度表與維度欄位關聯表 """
    __db_tabel_name__ = "metric_table_field"
    storage_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    table_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    field_id: UUID = SQLBaseEntityField(default_factory=uuid4)
