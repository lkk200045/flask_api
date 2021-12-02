# -*- coding: utf-8 -*-
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class StorageProviderEntity(SQLBaseEntityModel):
    """ 企業與數據來源關聯表 """
    __db_tabel_name__ = "storage_provider"
    storage_id: UUID = SQLBaseEntityField(default_factory=uuid4)
    account_id: UUID = SQLBaseEntityField(default_factory=uuid4)
