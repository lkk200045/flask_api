# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricCatalogProviderEntity(SQLBaseEntityModel):
    """ 企業與分類標籤關聯表 """
    __db_tabel_name__ = "metric_catalog_provider"
    catalog_tag_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    account_id: UUID = SQLBaseEntityField(default_factory=uuid4)
