# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class ProviderAccountEntity(SQLBaseEntityModel):
    """ 企業資料 """
    __db_tabel_name__ = "provider_account"
    account_id: UUID = SQLBaseEntityField(default_factory=uuid4, updatable=False, pk=True)
    account_name: Optional[str]  # 企業名稱
