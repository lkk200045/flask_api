# -*- coding: utf-8 -*-
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
from model import BaseSupportModel
from model.enums import StatusType
from model.metric_field import MetricFieldInsertModel
from datetime import datetime
from eyesmediapyutils.datetime import DEFAULT_DATETIME_PATTERN

logger = logging.getLogger("application")

class MetricTableInsertModel(BaseModel):
    id: Optional[str]
    name: str
    alias_name: str = Field(alias="aliasName")
    description: Optional[str]
    is_disabled: Optional[str] = Field(alias="isDisabled")
    table_type: Optional[str]= Field(alias="tableType")
    table_format: Optional[str]= Field(alias="tableFormat")
    fields:Optional[list[MetricFieldInsertModel]]= Field(alias="fields")

    def get_status_disabled_type(self):
        if self.is_disabled is not None:
            if self.is_disabled:
                return StatusType.DISABLE.value
            return StatusType.ENABLE.value
        return None

class MetricTableResModel(BaseModel):
    id: str
    name: str
    alias_name: str = Field(alias="aliasName")
    is_disabled: bool = Field(False, alias="isDisabled")
    storage_id: Optional[str] = Field(alias="storageId")
    storage_type_name: Optional[str] = Field(alias="storageTypeName")
    storage_name: Optional[str] = Field(alias="storageName")
    storage_alias_name: Optional[str] = Field(alias="storageAliasName")
    account_id: Optional[str] = Field(alias="accountId")
    account_name: Optional[str] = Field(alias="accountName")

    def get_status_disabled_type(self):
        if self.is_disabled is not None:
            if self.is_disabled:
                return StatusType.DISABLE.value
            return StatusType.ENABLE.value
        return None

class MetricSearchTableModel(BaseSupportModel):
    table_id: Optional[str] = Field(alias="tableId")
    table_name: Optional[str] = Field(alias="tableName")
    table_alias: Optional[str] = Field(alias="tableAlias")
    is_disabled: Optional[bool] = Field(False, alias="isDisabled")
    storage_type: Optional[str] = Field(False, alias="storageType")

    class Config(BaseSupportModel.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(DEFAULT_DATETIME_PATTERN)
        }
