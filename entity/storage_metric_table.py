# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class StorageMetricTableEntity(SQLBaseEntityModel):
    """ 數據來源與維度表關聯表 """
    __db_tabel_name__ = "storage_metric_table"
    storage_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    table_id: UUID = SQLBaseEntityField(default_factory=uuid4)
