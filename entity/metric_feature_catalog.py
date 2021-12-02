# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricFeatureCatalogEntity(SQLBaseEntityModel):
    """ 特徵標籤與分類標籤關聯表 """
    __db_tabel_name__ = "metric_feature_catalog"
    feature_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    catalog_tag_id: UUID = SQLBaseEntityField(default_factory=uuid4)
