import logging
import traceback

from eyesmediapyutils.page import Paging
import repository
from model.storage_info import StorageInfoModel
from typing import List, Tuple


logger = logging.getLogger("eyesmediapydb")
class StorageDao(repository.MySQLRepository):
    def insert_storage(self, Storage_info_object: StorageInfoModel, connection):
        sql = "INSERT INTO storage_info \
                value (%(storage_id)s\
                ,%(storage_type)s\
                ,%(storage_name)s\
                ,%(storage_alias)s\
                ,%(storage_account)s\
                ,%(storage_pwd)s\
                ,%(storage_host)s\
                ,%(storage_port)s\
                ,%(storage_url)s\
                ,%(storage_description)s\
                ,%(is_disabled)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "storage_id": Storage_info_object.storage_id,
            "storage_type": Storage_info_object.storage_type_code,
            "storage_name": Storage_info_object.storage_name,
            "storage_alias": Storage_info_object.storage_alias,
            "storage_account": Storage_info_object.connect_info.account,
            "storage_pwd": Storage_info_object.connect_info.pwd,
            "storage_host": Storage_info_object.connect_info.host,
            "storage_port": Storage_info_object.connect_info.port,
            "storage_url": Storage_info_object.connect_info.url,
            "storage_description": Storage_info_object.storage_description,
            "is_disabled": 0,
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)

    def insert_check(self, storage_type: str, storage_name: str):
        sql = "SELECT count(*)" \
              " FROM storage_info " \
              " WHERE storage_type = %(storage_type)s and storage_name = %(storage_name)s"
        params = {"storage_type": storage_type, "storage_name": storage_name}
        list = self.find(sql, params=params)
        return list

    def update_storage_info_data(self, id: str, update_column_name: str, value: str):
        sql = f''' UPDATE storage_info SET {update_column_name} = "{value}" WHERE storage_id= "{id}" '''
        try:
            connection = self.mysql_client.open_connection()
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        except:
            connection.rollback()
            logging.error(traceback.format_exc())
            raise
        finally:
            self.mysql_client.close_connection(connection)
        return id
    
    def get_counts(self, req_model: object) -> int:
        names = []
        accounts= []
        storage_names = str(req_model.storage_name).split(' ')
        for i in storage_names:
            names.append(i)
        account_names = str(req_model.account_name).split(' ')
        for i in account_names:
            accounts.append(i)
        sql, params = self.__search_storage_info_data(
            offset = None,
            limit = None,
            names = names,
            types = req_model.storage_type,
            accounts = accounts,
        )
        return self.count(sql, params=params)

    def find_with_paging(self,paging: object, req_model: object) -> List[dict]:
        offset=paging.start
        limit=paging.limit
        names = []
        accounts= []
        storage_names = str(req_model.storage_name).split(' ')
        for i in storage_names:
            names.append(i)
        account_names = str(req_model.account_name).split(' ')
        for i in account_names:
            accounts.append(i)
        sql, params = self.__search_storage_info_data(offset,limit,names,req_model.storage_type,accounts)
        return self.find(sql, params=params)


    def __search_storage_info_data(self,offset: str,limit: str,names: list,types: list,accounts: list)-> List[dict]:
        storage_names = names
        storage_types =  types
        account_names = accounts
        sql = "SELECT" \
              " storage_info.storage_id,storage_info.storage_type,storage_info.storage_name,storage_info.mdy_date,storage_provider.account_name,count(storage_metric_table.cnt) as table_count ,count(storage_provider.cnt2) as provider_count " \
              " FROM storage_info as storage_info" \
              " LEFT JOIN(select storage_id,count(storage_metric_table.table_id)as cnt from storage_metric_table group by table_id)as storage_metric_table \
                on storage_info.storage_id = storage_metric_table.storage_id" \
              " LEFT JOIN(select storage_provider.storage_id,provider_account.account_name,count(storage_provider.account_id)as cnt2 from storage_provider  \
                left join provider_account  on provider_account.account_id = storage_provider.account_id group by storage_id)as storage_provider \
                on storage_info.storage_id = storage_provider.storage_id" \
              " WHERE 1=1"
        params = dict()
        
        if len(storage_names) > 0:
            key = "storage_name"
            storage_name = '%'+str(storage_names[0])+'%'
            sql += " AND storage_name LIKE  %(storage_name)s".format(storage_name)
            params.setdefault(key,storage_name)
        for i in range(1,len(storage_names)):
            key = "storage_name"+str(i)
            storage_names[i] = '%'+str(storage_names[i])+'%'
            sql +="or storage_name LIKE  %(storage_name1)s".format(storage_names[i])
            params.setdefault(key,storage_names[i])
        if len(storage_types) > 0:
            key = "storage_type"
            sql += " or storage_type =  %(storage_type)s".format(storage_types[0])
            params.setdefault(key,storage_types[0])
        for i in range(1,len(storage_types)):
            key = "storage_type"+str(i)
            sql +=" or storage_type = %(storage_type1)s"
            params.setdefault(key,storage_types[i])
        if len(account_names) > 0:
            key = "account_name"
            account_name = '%'+str(account_names[0])+'%'
            sql += " or storage_provider.account_name LIKE  %(account_name)s".format(account_names[0])
            params.setdefault(key,account_name)
        for i in range(1,len(account_names)):
            key = "account_name"+str(i)
            account_names[i] = '%'+str(account_names[i])+'%'
            sql +="or storage_provider.account_name LIKE  %(account_name1)s".format(account_names[i])
            params.setdefault(key,account_names[i])
        sql += " group by storage_id"
         # 排序
        sql += " ORDER BY storage_info.storage_id"
        # 設定分頁 SQL
        if limit is not None:
            sql += " limit %(limit)s"
            params.setdefault("limit", limit)
        if offset is not None:
            sql += " offset %(offset)s"
            params.setdefault("offset", offset)
        return sql,params

    def search_storage_info(self,storage_id: str)-> List[dict]:
        params = dict()
        sql = " select storage_info.*,provider.account_name,mertic.table_name,mertic.table_alias,provider.account_id,mertic.table_id,mertic.is_disabled " \
              " from storage_info " \
              " left join(SELECT storage_provider.storage_id,provider_account.account_name,provider_account.account_id FROM storage_provider left join provider_account on storage_provider.account_id = provider_account.account_id)as provider " \
              " on storage_info.storage_id = provider.storage_id " \
              " left join(SELECT storage_metric_table.storage_id,storage_metric_table.table_id,metric_table.table_alias,metric_table.table_name,metric_table.is_disabled FROM storage_metric_table left join metric_table on storage_metric_table.table_id= metric_table.table_id)as mertic " \
              " on storage_info.storage_id = mertic.storage_id " \
              " where storage_info.storage_id = %(storage_id)s"
        params.setdefault("storage_id",storage_id)
        list = self.find(sql, params=params)
        return list

