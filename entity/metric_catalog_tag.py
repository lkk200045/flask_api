# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricCatalogTagEntity(SQLBaseEntityModel):
    """ 分類標籤主表 """
    __db_tabel_name__ = "metric_catalog_tag"
    tag_id: UUID = SQLBaseEntityField(default_factory=uuid4, pk=True)
    tag_parent_id: Optional[str]
    tag_code: str  # 維度主題領域代碼
    tag_name: str  # 維度主題領域名稱
    tag_type: str  # 分類標籤類型：BASE(基礎) / RULE(規則)
    tag_description: Optional[str]  # 維度主題領域簡述
    is_disabled: Optional[int] = 0  # 停用註記：0(不停用)/1(停用)