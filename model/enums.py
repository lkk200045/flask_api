# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class StatusType(Enum):
    ENABLE = 0
    DISABLE = 1


class StorageType(Enum):
    STORAGE_TYPE_MYSQL = "MySQL"
    STORAGE_TYPE_MONGODB = "MongoDB"
    TABLE_TYPE_TABLE = "Table"
    TABLE_TYPE_COLLECTION = "Collection"
    TABLE_FORMAT_TABLE = "Table"
    TABLE_FORMAT_JSON = "JSON"


class TableType(Enum):
    TABLE_TYPE_TABLE = "Table"
    TABLE_TYPE_COLLECTION = "Collection"
    TABLE_FORMAT_TABLE = "Table"
    TABLE_FORMAT_JSON = "JSON"


@unique
class CatalogTagType(Enum):
    """ 分類標籤類型 """
    BASE = "BASE"  # 基礎
    RULE = "RULE"  # 規則


class UpdateType(Enum):
    UPDATE_TYPE_ACCOUNT = "accountId"
    UPDATE_TYPE_TABLE = "tableId"


class ProviderMetricUpdateAction(Enum):
    UPDATE_ACTION_INSERT = "new"
    UPDATE_ACTION_DELETE = "delete"


@unique
class GenericConstantGroupCode(str, Enum):
    """ 共用元件(下拉式選單/autocomplete)群組代碼 """
    STORAGE_TYPE = "STORAGE_TYPE"  # 數據來源種類
    TABLE_TYPE = "TABLE_TYPE"  # 維度表類型
    TABLE_FORMAT = "TABLE_FORMAT"  # 維度表格式
    FIELD_TYPE = "FIELD_TYPE"  # 維度欄位類型
    BIZ_ACCOUNT = "BIZ_ACCOUNT"  # 歸屬企業
    METRIC_TABLE = "METRIC_TABLE"  # 維度表

    @classmethod
    def has_value(self, value):
        return value in self._value2member_map_

    def is_biz_account(self):
        return self == GenericConstantGroupCode.BIZ_ACCOUNT

    def is_metric_table(self):
        return self == GenericConstantGroupCode.METRIC_TABLE


@unique
class HTMLInputColumnName(Enum):
    NAME = "NAME"
    ALIAS = "ALIAS"
    TYPE = "TYPE"
    LENGTH = "LENGTH"
    DEFAULE = "DEFAULE"
    DESCRIPTION = "DESCRIPTION"
    DISABLED = "DISABLED"
    REQUIRED = "REQUIRED"

    def parse_value(self, value):
        return {
            self.NAME: str(value),
            self.ALIAS: str(value),
            self.TYPE: str(value),
            self.LENGTH: int(value),
            self.DEFAULE: str(value),
            self.DESCRIPTION: str(value),
            self.DISABLED: bool(value),
            self.REQUIRED: bool(value)
        }[self]
