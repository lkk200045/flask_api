# -*- coding: utf-8 -*-
import logging
from config.application import ApplicationContext
from config.constants import MONGODB_AUTH_MODE_SHA1

logger = logging.getLogger("application")


class FeatureHandleService():

    def __init__(self, app_context: ApplicationContext):
        self.app_context = app_context

    def connect_config_mongoDB(self, connect_info: object, storage_name: str):
        input_config = {
            "host": connect_info.host,
            "port": int(connect_info.port),
            "dbname": storage_name,
            "username": connect_info.account,
            "pwd": connect_info.pwd,
        }
        input_config.setdefault("authentication-database", input_config["dbname"])
        input_config.setdefault("authentication-mode", MONGODB_AUTH_MODE_SHA1)
        provider = self.app_context.init_mongo_client(input_config)
        return provider

    def init_other_mysql(self, connect_info: object, storage_name: str):
        config = {
            'host': connect_info.host,
            "port": int(connect_info.port),
            "dbname": storage_name,
            "username": connect_info.account,
            "password": connect_info.pwd
        }
        provider = self.app_context.init_mysql_client(config)
        return provider
