# -*- coding: utf-8 -*-
import logging
from enum import Enum, unique
from datetime import datetime
from typing import (Any, Optional, Tuple)
from pydantic import BaseModel
from pydantic.fields import (Undefined, NoArgAnyCallable, FieldInfo)
from uuid import UUID

logger = logging.getLogger("eyesmediapydb")


class SystmeUser(Enum):
    USER_ID = "SYSTEM"
    USER_NAME = "SYSTEM"


@unique
class SQLBaseEntityFieldName(Enum):
    INSERTABLE = "insertable"
    UPDATABLE = "updatable"
    PK = "pk"
    USE_SQL_DATETIME = "use_sql_datetime"


def SQLBaseEntityField(
        default: Any = Undefined,
        *,
        default_factory: Optional[NoArgAnyCallable] = None,
        alias: str = None,
        title: str = None,
        description: str = None,
        const: bool = None,
        gt: float = None,
        ge: float = None,
        lt: float = None,
        le: float = None,
        multiple_of: float = None,
        min_items: int = None,
        max_items: int = None,
        min_length: int = None,
        max_length: int = None,
        allow_mutation: bool = True,
        insertable: bool = True,
        updatable: bool = True,
        pk: bool = False,
        use_sql_datetime: bool = False,
        regex: str = None,
        **extra: Any,
) -> Any:
    field_info = FieldInfo(
        default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        min_items=min_items,
        max_items=max_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        insertable=insertable,
        updatable=updatable,
        pk=pk,
        use_sql_datetime=use_sql_datetime,
        **extra,
    )
    field_info._validate()
    return field_info


class SQLBaseEntityModel(BaseModel):
    __db_tabel_name__ = None

    crt_user_id: Optional[str] = SQLBaseEntityField(SystmeUser.USER_ID, updatable=False)  # 新增人員
    crt_user_name: Optional[str] = SQLBaseEntityField(SystmeUser.USER_NAME, updatable=False)
    crt_date: Optional[datetime] = SQLBaseEntityField(default_factory=datetime.utcnow, updatable=False, use_sql_datetime=False)  # 新增時間
    mdy_user_id: Optional[str] = SQLBaseEntityField(SystmeUser.USER_ID)  # 異動人員
    mdy_user_name: Optional[str] = SQLBaseEntityField(SystmeUser.USER_NAME)
    mdy_date: Optional[datetime] = SQLBaseEntityField(default_factory=datetime.utcnow, use_sql_datetime=False)  # 異動時間

    class Config:
        use_enum_values = True

    def __has_pk_attr(self, cls):
        return self.__fields__.get(cls).field_info.extra.get(SQLBaseEntityFieldName.PK.value, False)

    def __has_insertable_attr(self, cls):
        return self.__fields__.get(cls).field_info.extra.get(SQLBaseEntityFieldName.INSERTABLE.value, True)

    def __has_updatable_attr(self, cls):
        return self.__fields__.get(cls).field_info.extra.get(SQLBaseEntityFieldName.UPDATABLE.value, True)

    def __use_sql_datetime(self, cls):
        return self.__fields__.get(cls).field_info.extra.get(SQLBaseEntityFieldName.USE_SQL_DATETIME.value, False)

    def __cls_value_to_str(self, cls_value):
        if isinstance(cls_value, UUID):
            return str(cls_value)
        return cls_value

    def __cls_to_where_sql(self, cls: dict) -> Tuple[str, dict]:
        column_len = len(cls) if cls is not None else 0
        if column_len == 0:
            return "", dict()
        sql = " WHERE "
        params = dict()
        column_idx = 0
        for attr_name, attr_val in cls.items():
            sql += attr_name + " = %(" + attr_name + ")s"
            if column_idx + 1 < column_len:
                column_idx += 1
                sql += " AND "
            params.setdefault(attr_name, self.__cls_value_to_str(attr_val))
        return sql, params

    def _to_insert_sql(self) -> Tuple[str, dict]:
        sql = "INSERT INTO " + self.__db_tabel_name__ + " ("
        column_idx = 0
        column_len = len(self.dict())
        params = dict()
        value_key = ""
        for attr_name, attr_val in self.dict().items():
            # 略過不需要新增的欄位
            if not self.__has_insertable_attr(attr_name):
                column_idx += 1
                continue
            # 添加 colunm name SQL
            sql += attr_name
            if self.__use_sql_datetime(attr_name):
                value_key += "now()"
            else:
                value_key += "%(" + attr_name + ")s"
                params.setdefault(attr_name, self.__cls_value_to_str(attr_val))
            # 添加分隔 SQL
            if column_idx + 1 < column_len:
                column_idx += 1
                sql += ","
                value_key += ","
        sql += ") VALUES (" + value_key + ")"
        return sql, params

    def _to_update_where_pk_sql(self) -> Tuple[str, dict]:
        sql = "UPDATE " + self.__db_tabel_name__ + " SET "
        column_idx = 0
        column_len = len(self.dict())
        params = dict()
        pk_cls = dict()
        for attr_name, attr_val in self.dict().items():
            # 捕抓 PK 欄位
            if self.__has_pk_attr(attr_name):
                pk_cls.setdefault(attr_name, self.__cls_value_to_str(attr_val))
            # 略過不需要更新的欄位
            if not self.__has_updatable_attr(attr_name):
                column_idx += 1
                continue
            # 添加 colunm name SQL
            if self.__use_sql_datetime(attr_name):
                sql += attr_name + " = now()"
            else:
                sql += attr_name + " = %(" + attr_name + ")s"
                params.setdefault(attr_name, self.__cls_value_to_str(attr_val))
            # 添加分隔 SQL
            if column_idx + 1 < column_len:
                column_idx += 1
                sql += ","
        # 根據 PK 添加 WHERE SQL
        if pk_cls is None or len(pk_cls) == 0:
            raise ValueError("not found PK columns...")
        where_sql, where_params = self.__cls_to_where_sql(pk_cls)
        sql += where_sql
        params.update(where_params)
        return sql, params

    def _to_delete_by_pk_sql(self) -> Tuple[str, dict]:
        sql = "DELETE FROM " + self.__db_tabel_name__
        params = dict()
        pk_cls = {attr_name: self.__cls_value_to_str(attr_val) for attr_name, attr_val in self.dict().items() if self.__has_pk_attr(attr_name)}
        # 根據 PK 添加 WHERE SQL
        if pk_cls is None or len(pk_cls) == 0:
            raise ValueError("not found PK columns...")
        where_sql, where_params = self.__cls_to_where_sql(pk_cls)
        sql += where_sql
        params.update(where_params)
        return sql, params
