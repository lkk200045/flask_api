# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import Field
from entity import SQLBaseEntityModel


class MetricCatalogRelationEntity(SQLBaseEntityModel):
    """ 分類標籤關係表 """
    __db_tabel_name__ = "metric_catalog_relation"
    source_catalog_tag_id: str
    sink_catalog_tag_id: str


