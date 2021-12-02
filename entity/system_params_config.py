# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class SystemParamsConfigEntity(SQLBaseEntityModel):
    """ 系統常數標籤表 """
    __db_tabel_name__ = "system_params_config"
    config_id: UUID = SQLBaseEntityField(default_factory=uuid4, updatable=False, pk=True)
    config_parent_code: Optional[str]
    group_code: Optional[str] = SQLBaseEntityField(updatable=False)  # 系統常數標籤群組代碼
    config_code: str = SQLBaseEntityField(updatable=False)  # 系統常數標籤代碼
    config_name: str  # 系統常數標籤名稱
    is_disabled: Optional[int] = 0  # 是否停用
