# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricFieldCatalogEntity(SQLBaseEntityModel):
    """ 維度欄位與分類標籤關聯表 """
    __db_tabel_name__ = "metric_field_catalog"
    field_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    catalog_tag_id: UUID = SQLBaseEntityField(default_factory=uuid4)
