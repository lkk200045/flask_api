# -*- coding: utf-8 -*-
import abc
import logging
import time
import traceback
from enum import Enum, unique
from typing import List, Tuple
from pymysql.connections import Connection
from eyesmediapydb.mysql_base import MySqlConnectionProvider
from entity import SQLBaseEntityModel

logger = logging.getLogger("eyesmediapydb")


@unique
class SQLExcuteType(Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SELECT = "SELECT"


class MySQLRepository(abc.ABC):

    def __init__(self, mysql_client: MySqlConnectionProvider):
        self.mysql_client = mysql_client

    def open_connection(self):
        connection = self.mysql_client.open_connection()
        connection.autocommit(False)
        connection.begin()
        return connection

    def rollback_connection(self, connection):
        try:
            if connection is not None:
                connection.rollback()
                logger.debug("connection({}) rollback...".format(connection))
        except:
            pass

    def close_connection(self, connection):
        self.mysql_client.close_connection(connection)

    def excute_sql(self, sql: str, params, multiple=False, connection: Connection = None):
        """
        執行 SQL 語法(含 transaction 機制)

        Args:
            sql: SQL
            params: 參數
            multiple: 執行多筆為 True，單筆為 False(預設)
            connection: pymysql.connections.Connection，未傳入時會另開新的連線物件

        """
        logger.debug("{}\n{}".format(sql, params))
        _connection = connection
        new_connet = False
        try:
            if _connection is None:
                _connection = self.open_connection()
                new_connet = True
            logger.debug("connection({}) new:{}".format(_connection, new_connet))
            with _connection.cursor() as cursor:
                if multiple:
                    cursor.executemany(sql, args=params)
                else:
                    cursor.execute(sql, args=params)
            if new_connet:
                _connection.commit()
        except:
            if new_connet:
                self.rollback_connection(_connection)
                logger.error("connection({}) error: {}\n{}\n".format(_connection, sql, params))
            logger.error(traceback.format_exc())
            raise
        finally:
            if new_connet:
                self.close_connection(_connection)

    def count(self, sql: str, params=None, connection: Connection = None) -> int:
        tbname = "table" + str(time.time_ns())
        count_sql = "select count(*) as cnt from ({}) as {}".format(sql, tbname)
        datas = self.find(sql=count_sql, params=params, connection=connection)
        return datas[0]["cnt"] if datas and len(datas) > 0 else 0

    def find(self, sql: str, params=None, offset: int = None, limit: int = None, connection: Connection = None) -> List[dict]:
        if params is None:
            params = dict()
        if limit is not None:
            sql += " limit %(limit)s"
            params.setdefault("limit", limit)
        if offset is not None:
            sql += " offset %(offset)s"
            params.setdefault("offset", offset)
        logger.debug("{}\n{}".format(sql, params))

        _connection = connection
        new_connet = False
        try:
            if _connection is None:
                _connection = self.mysql_client.open_connection()
                new_connet = True
            logger.debug("connection({}) new:{}".format(_connection, new_connet))
            with _connection.cursor() as cursor:
                cursor.execute(sql, args=params)
                rows = cursor.fetchall()
                rownumber = cursor.rownumber
        except:
            logger.error("connection({}) error: {}\n{}\n".format(_connection, sql, params))
            logger.error(traceback.format_exc())
            raise
        finally:
            if new_connet:
                self.mysql_client.close_connection(_connection)
        return list() if rownumber == 0 else rows

    def __generate_sql_and_params(self, db_entity: SQLBaseEntityModel, excute_type: SQLExcuteType) -> Tuple[str, dict]:
        if SQLExcuteType.INSERT == excute_type:
            return db_entity._to_insert_sql()
        if SQLExcuteType.UPDATE == excute_type:
            return db_entity._to_update_where_pk_sql()
        if SQLExcuteType.DELETE == excute_type:
            return db_entity._to_delete_by_pk_sql()
        raise ValueError("excute type must be INSERT, UPDATE, DELETE.")

    def __generate_multiple_sql_and_params(self, db_entities: List[SQLBaseEntityModel], excute_type: SQLExcuteType) -> Tuple[str, List[dict]]:
        params = list()
        sql = None
        for db_entity in db_entities:
            sql, _params = self.__generate_sql_and_params(db_entity=db_entity, excute_type=excute_type)
            params.append(_params)
        return sql, params

    def __excute(self, db_entities: List[SQLBaseEntityModel], excute_type: SQLExcuteType, connection: Connection = None):
        if db_entities is None or len(db_entities) == 0:
            logger.warning("not found any excute db entities, do nothing...")
            return
        is_multiple = len(db_entities) > 1
        if is_multiple:
            sql, params = self.__generate_multiple_sql_and_params(db_entities, excute_type)
        else:
            if db_entities[0] is None:
                logger.warning("not found any excute db entities, do nothing...")
                return
            sql, params = self.__generate_sql_and_params(db_entities[0], excute_type)
        self.excute_sql(sql=sql, params=params, multiple=is_multiple, connection=connection)

    def insert(self, db_entity: SQLBaseEntityModel, connection: Connection = None):
        """ 單筆新增 """
        self.__excute(db_entities=[db_entity], excute_type=SQLExcuteType.INSERT, connection=connection)

    def insert_many(self, db_entities: List[SQLBaseEntityModel], connection: Connection = None):
        """ 多筆新增 """
        self.__excute(db_entities=db_entities, excute_type=SQLExcuteType.INSERT, connection=connection)

    def update_by_pk(self, db_entity: SQLBaseEntityModel, connection: Connection = None):
        """ 單筆更新(根據主鍵) """
        self.__excute(db_entities=[db_entity], excute_type=SQLExcuteType.UPDATE, connection=connection)

    def update_many_by_pk(self, db_entities: List[SQLBaseEntityModel], connection: Connection = None):
        """ 多筆更新(根據多筆主鍵) """
        self.__excute(db_entities=db_entities, excute_type=SQLExcuteType.UPDATE, connection=connection)

    def delete_by_pk(self, db_entity: SQLBaseEntityModel, connection: Connection = None):
        """ 單筆刪除(根據主鍵) """
        self.__excute(db_entities=[db_entity], excute_type=SQLExcuteType.DELETE, connection=connection)

    def delete_many_by_pk(self, db_entities: List[SQLBaseEntityModel], connection: Connection = None):
        """ 多筆刪除(根據多筆主鍵) """
        self.__excute(db_entities=db_entities, excute_type=SQLExcuteType.DELETE, connection=connection)
