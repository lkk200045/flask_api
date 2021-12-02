import logging
import repository
import traceback
from model.storage_info import StorageInfoModel, StorageProviderMetricTablUpdateModel


class StorageProviderDao(repository.MySQLRepository):
    def insert_storage_provider(self, Storage_info_object: StorageInfoModel, account_id: str, connection):
        sql = "INSERT INTO storage_provider \
                value (%(storage_id)s\
                ,%(account_id)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "storage_id": Storage_info_object.storage_id,
            "account_id": account_id,
            "crt_user_id": Storage_info_object.user_id,
            "crt_user_name": Storage_info_object.user_name,
            "mdy_user_id": Storage_info_object.user_id,
            "mdy_user_name": Storage_info_object.user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)

    def delete_storage_provider_data(self, storage_id: str, account_id: str):
        sql = f''' delete from storage_provider WHERE storage_id= "{storage_id}" AND account_id = "{account_id}" '''
        logging.error(sql)
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
        return storage_id

    def update_storage_provider_data(self, storage_id: str, account_id: str, user_name: str, user_id: str):
        providerItem = StorageProviderMetricTablUpdateModel()
        providerItem.storage_id = storage_id
        providerItem.user_name = user_name
        providerItem.user_id = user_id
        try:
            connection = self.mysql_client.open_connection()
            self.insert_storage_provider(providerItem, account_id, connection)
            connection.commit()
        except:
            connection.rollback()
            logging.error(traceback.format_exc())
            raise
        finally:
            self.mysql_client.close_connection(connection)
        return storage_id
