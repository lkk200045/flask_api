# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricFeatureEntity(SQLBaseEntityModel):
    """ 特徵標籤主表 """
    __db_tabel_name__ = "metric_feature"
    feature_id: UUID = SQLBaseEntityField(default_factory=uuid4, updatable=False, pk=True)
    feature_label: str  # 特徵名稱
    feature_value: str  # 特徵數值
    is_disabled: Optional[int] = 0  # 停用註記：0(不停用)/1(停用)
