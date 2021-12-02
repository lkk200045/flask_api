# -*- coding: utf-8 -*-
from entity import SQLBaseEntityModel


class MetricFeatureRelationEntity(SQLBaseEntityModel):
    """ 特徵標籤關係表 """
    __db_tabel_name__ = "metric_feature_relation"
    source_feature_id: str
    sink_feature_id: str
