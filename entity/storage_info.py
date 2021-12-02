# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID, uuid4
from entity import SQLBaseEntityField
from entity import SQLBaseEntityModel


class StorageInfoEntity(SQLBaseEntityModel):
    """ 數據來源資訊 """
    __db_tabel_name__ = "storage_info"
    storage_id: UUID = SQLBaseEntityField(default_factory=uuid4, pk=True)
    storage_type: str  # 儲存庫類型：MYSQL/MONGO/S3/REDIS
    storage_name: str  # 儲存庫名稱
    storage_alias: str  # 儲存庫別名
    storage_account: Optional[str]  # 儲存庫登入帳號
    storage_pwd: Optional[str]  # 儲存庫登入密碼
    storage_host: Optional[str]  # 儲存庫host
    storage_port: Optional[int]  # 儲存庫埠號
    storage_url: Optional[str]  # 儲存庫URL位置
    storage_description: Optional[str]  # 儲存庫簡述
    is_disabled: Optional[int] = 0  # 停用註記：0(不停用)/1(停用)
