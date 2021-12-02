# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricFieldFeatureEntity(SQLBaseEntityModel):
    """ 維度欄位與特徵標籤關聯表 """
    __db_tabel_name__ = "metric_field_feature"
    field_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    feature_id: UUID = SQLBaseEntityField(default_factory=uuid4)
