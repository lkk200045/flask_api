# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class MetricTableEntity(SQLBaseEntityModel):
    """ 維度表資訊 """
    __db_tabel_name__ = "metric_table"
    table_id: UUID = SQLBaseEntityField(default_factory=uuid4, pk=True)
    table_name: str  # 維度表名稱
    table_alias: str  # 維度表別名
    table_type: str  # 資料類型：TABLE(數據表)/DOC(文件)
    table_format: str  # 表格式：TABLE(數據表)/JSON/CSV
    table_description: Optional[str]  # 維度表簡述
    is_disabled: Optional[int] = 0  # 停用註記：0(不停用)/1(停用)
