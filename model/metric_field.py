# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID
from pydantic import Field
from model import BaseSupportModel
from model import BaseDateTimeFormatSupportModel
from model.enums import StatusType, CatalogTagType

logger = logging.getLogger("application")


class MetricFieldTableModel(BaseSupportModel):
    """ 維度表 """
    table_id: Optional[Union[UUID, str]] = Field(alias="id")
    table_name: Optional[str] = Field(alias="name")
    table_alias: Optional[str] = Field(alias="aliasName")
    is_disabled: Optional[bool] = Field(False, alias="isDisabled")
    storage_id: Optional[str] = Field(alias="storageId")
    storage_type: Optional[str] = Field(alias="storageTypeName")
    storage_name: Optional[str] = Field(alias="storageName")
    storage_alias: Optional[str] = Field(alias="storageAliasName")
    account_id: Optional[str] = Field(alias="accountId")
    account_name: Optional[str] = Field(alias="accountName")


class MetricFieldFeatureModel(BaseSupportModel):
    """ 維度特徵 """
    feature_id: Optional[Union[UUID, str]] = Field(alias="id")
    feature_label: Optional[str] = Field(alias="label")
    feature_value: Optional[str] = Field(alias="value")
    is_disabled: Optional[bool] = Field(False, alias="isDisabled")


class MetricCatalogTagModel(BaseSupportModel):
    """ 分類標籤 """
    tag_id: Optional[Union[UUID, str]] = Field(alias="id")
    tag_parent_id: Optional[str] = Field(alias="parentId")
    tag_code: str = Field(alias="code")  # 維度主題領域代碼
    tag_name: str = Field(alias="name")  # 維度主題領域名稱
    tag_type: str = Field(CatalogTagType.BASE, alias="type")  # 分類標籤類型：BASE(基礎) / RULE(規則)
    tag_description: Optional[str] = Field(alias="description")  # 維度主題領域簡述
    is_disabled: Optional[bool] = Field(False, alias="isDisabled")  # 停用註記
    tag_path: Optional[str] = Field(alias="path")  # 包含根分類以及所有上層分類


class MetricFieldModel(BaseDateTimeFormatSupportModel):
    """ 維度表明細 """
    field_id: Union[UUID, str] = Field(alias="id")
    field_name: str = Field(alias="name")
    field_alias: str = Field(alias="aliasName")
    field_type: str = Field(alias="typeCode")
    field_length: Optional[int] = Field(alias="length")
    field_default_value: Optional[str] = Field(alias="defaultValue")
    is_required: bool = Field(False, alias="isRequired")
    is_disabled: bool = Field(False, alias="isDisabled")
    field_description: Optional[str] = Field(alias="description")
    table: Optional[MetricFieldTableModel]
    catalog: Optional[MetricCatalogTagModel]
    features: Optional[List[MetricFieldFeatureModel]]
    mdy_user_id: str = Field(None, alias="mdyUserId")
    mdy_user_name: str = Field(None, alias="mdyUserName")
    mdy_date: datetime = Field(None, alias="mdyDate")


class MetricFieldInsertModel(BaseSupportModel):
    id: Optional[str]
    name: Optional[str]
    alias_name: str = Field(alias="aliasName")
    field_type: Optional[str] = Field(alias="typeCode")
    field_type_name: Optional[str] = Field(alias="typeName")
    field_length: Optional[str] = Field(alias="length")
    field_default_value: Optional[str] = Field(alias="defaultValue")
    field_description: Optional[str] = Field(alias="description")
    is_required: Optional[str] = Field(alias="isRequired")
    is_disabled: Optional[str] = Field(alias="isDisabled")
    feature_count: Optional[int] = Field(alias="featureCount")
    catalog_tag_id: Optional[list[str]] = Field(alias="catalogTagId")

    def get_status_disabled_type(self):
        if self.is_disabled is not None:
            if self.is_disabled:
                return StatusType.DISABLE.value
            return StatusType.ENABLE.value
        return None

    def get_status_required_type(self):
        if self.is_required is not None:
            if self.is_required:
                return StatusType.DISABLE.value
            return StatusType.ENABLE.value
        return None


class MetricFieldSearchReqModel(BaseSupportModel):
    """ 列表查詢 request model """
    name: Optional[str]
    storage_type_code: Optional[List[str]] = Field(alias="storageTypeCode")
    table_type_code: Optional[List[str]] = Field(alias="tableTypeCode")
    account_name: Optional[str] = Field(alias="accountName")
    is_disabled: Optional[bool] = Field(alias="isDisabled")
    page_no: Optional[int] = Field(1, alias="pageNo")
    limit: Optional[int] = 100

    def get_field_names(self):
        if self.name and len(self.name) > 0:
            return self.name.split(" ")
        return list()

    def get_account_names(self):
        if self.account_name and len(self.account_name) > 0:
            return self.account_name.split(" ")
        return list()

    def get_status_type(self):
        if self.is_disabled is not None:
            if self.is_disabled:
                return StatusType.DISABLE.value
            return StatusType.ENABLE.value
        return None


class MetricFieldSearchSummaryResModel(BaseSupportModel):
    """ 列表查詢 response model """
    catalog_counts: int = Field(0, alias="catalogCounts")
    feature_counts: int = Field(0, alias="featureCounts")


class MetricFieldSearchResModel(BaseDateTimeFormatSupportModel):
    """ 列表查詢 response model """
    field_id: Union[UUID, str] = Field(alias="id")
    field_name: str = Field(alias="name")
    field_alias: str = Field(alias="aliasName")
    field_type: str = Field(alias="typeCode")
    field_length: Optional[int] = Field(None, alias="length")
    is_disabled: bool = Field(False, alias="isDisabled")
    is_required: bool = Field(False, alias="isRequired")
    mdy_user_id: str = Field(None, alias="mdyUserId")
    mdy_user_name: str = Field(None, alias="mdyUserName")
    mdy_date: datetime = Field(None, alias="mdyDate")
    table: MetricFieldTableModel
    summary: MetricFieldSearchSummaryResModel


class MetricFieldNewReqModel(BaseSupportModel):
    """ 維度表新增 request model """
    field_name: str = Field(alias="name")
    field_alias: str = Field(alias="aliasName")
    field_type: str = Field(alias="typeCode")
    field_length: Optional[int] = Field(alias="length")
    field_default_value: Optional[str] = Field(alias="defaultValue")
    is_required: bool = Field(False, alias="isRequired")
    field_description: Optional[str] = Field(alias="description")
    table_id: str = Field(alias="tableId")
    tag_id: Optional[str] = Field(alias="catalogId")
    features: Optional[List[MetricFieldFeatureModel]]

    def has_features(self):
        return self.features is not None and len(self.features) > 0
