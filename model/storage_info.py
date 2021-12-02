import logging
from typing import Union,Set,Dict,List, Optional
from pydantic import BaseModel, Field
from model import BaseSupportModel
from model.connectInfo import connectInfoModel, connectInfoResModal
from model.metric_table import MetricSearchTableModel, MetricTableInsertModel
from datetime import datetime
from eyesmediapyutils.datetime import DEFAULT_DATETIME_PATTERN

from model.provider_account import ProviderAccountResModal


logger = logging.getLogger("application")

class StorageInfoModel(BaseModel):
    user_id: Optional[str] = Field(alias="userId")
    user_name: Optional[str] = Field(alias="userName")
    storage_id: Optional[str] = Field(alias="storageId")
    storage_type:Optional[str] = Field(alias="storageType")
    storage_name: Optional[str] = Field(alias="storageName")
    storage_alias: Optional[str] = Field(alias="storageAlias")
    storage_description: Optional[str] = Field(alias="storageDescription")
    connect_info: Optional[connectInfoModel] = Field(alias="connectInfo")
    account_id: Optional[List[str]] = Field(alias="accountId")
    data: Optional[List[MetricTableInsertModel]] = Field(alias="data")
    storage_type_code: Optional[str]
    table_type_code: Optional[str]
    table_type_format: Optional[str]


class StorageInfoUpdateModel(BaseModel):
    storage_id: Optional[str] = Field(alias="storageId")
    update_column_name: Optional[str] = Field(alias="updateColumnName")
    value: Optional[str] = Field(alias="value")


class StorageProviderMetricTablUpdateModel(BaseModel):
    storage_id: Optional[str]
    update_table: Optional[str]
    update_value: Optional[str]
    user_name:Optional[str] = Field(alias="userName")
    user_id:Optional[str] = Field(alias="userId")

class StorageSearchReqModal(BaseModel):
    storage_type: Optional[List[str]]= Field(alias="storageType")
    storage_name: Optional[str]= Field(alias="storageName")
    account_name: Optional[str]= Field(alias="accountName")
    status: Optional[str]= Field(alias="status")
    page_no: Optional[int]= Field(alias="pageNo")
    page_size: Optional[int]= Field(100,alias="pageSize")


class StorageSearchListResModal(BaseSupportModel):
    storage_id: str = Field(alias="storageId")
    storage_type: str = Field(alias="storageType")
    storage_name: str = Field(alias="storageName")
    storage_alias: str = Field(False, alias="storageAlias")
    is_disabled: bool = Field(False, alias="isDisabled")
    table_count: str = Field(None, alias="tableCount")
    provider_count: str = Field(None, alias="accountCount")
    mdy_date: datetime = Field(None, alias="mdyDate")
   

    class Config(BaseSupportModel.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(DEFAULT_DATETIME_PATTERN)
        }



class StorageSearchResModal(BaseSupportModel):
    storage_id: Optional[str] = Field(alias="storageId")
    storage_type: Optional[str] = Field(alias="storageType")
    storage_name: Optional[str] = Field(alias="storageName")
    storage_alias: Optional[str] = Field(False, alias="storageAlias")
    storage_description: Optional[str] = Field(False, alias="storageDescription")
    is_disabled: Optional[bool] = Field(False, alias="isDisabled")
    mdy_date: Optional[datetime] = Field(None, alias="mdyDate")
    connect_info: Optional[connectInfoResModal] = Field(alias="connectInfo")
    account: Optional[List[ProviderAccountResModal]]  = Field(alias="account")
    structure : Optional[List[MetricSearchTableModel]]  = Field(alias="structure")

    class Config(BaseSupportModel.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(DEFAULT_DATETIME_PATTERN)
        }



