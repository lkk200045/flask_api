# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class ProviderUserEntity(SQLBaseEntityModel):
    """ 企業用戶主表 """
    __db_tabel_name__ = "provider_user"
    provider_id: UUID = SQLBaseEntityField(default_factory=uuid4, pk=True)
    account_id: str  # 企業帳號ID
    user_id: str  # 艾斯用戶唯一識別碼
    user_name: Optional[str]  # 用戶姓名
