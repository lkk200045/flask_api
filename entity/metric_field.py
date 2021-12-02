# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityModel
from entity import SQLBaseEntityField


class MetricFieldEntity(SQLBaseEntityModel):
    """ 維度欄位 """
    __db_tabel_name__ = "metric_field"
    field_id: UUID = SQLBaseEntityField(default_factory=uuid4, updatable=False, pk=True)
    field_name: str
    field_alias: str
    field_type: Optional[str]
    field_length: Optional[int]
    field_default_value: Optional[str]
    is_required: int = 0
    is_disabled: int = 0
