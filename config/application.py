# -*- coding: utf-8 -*-
import yaml
import os
import logging
import logging.config
import traceback
import configparser
import time
from elasticsearch import Elasticsearch
from config import LOG_PATH, BOOTSTRAP_CONFIG_FILE, LOGGING_CONFIG_FILE, DEFAULT_CONFIG_FILE, DEFAULT_MESSAGE_FILE
from config import EnvVarLoader
from config.s3_config import S3ApplicationConfig
from config.constants import LanguageType
from config.cloud_config import load_config
from eyesmediapydb.mongo_base import MongoConfig, MongoClientProvider
from eyesmediapydb.mysql_base import MySqlConfig, MySqlConnectionProvider

logger = logging.getLogger("application")


def _init_logging():
    default_level = logging.NOTSET
    default_format = "%(asctime)s [%(threadName)s-%(process)d] %(levelname)-5s %(module)s - %(message)s"
    use_default = False

    if os.path.exists(LOGGING_CONFIG_FILE):
        if not os.path.isdir(LOG_PATH):
            os.mkdir(LOG_PATH)
        try:
            with open(LOGGING_CONFIG_FILE, encoding="utf-8") as file:
                log_setting = yaml.load(file, Loader=EnvVarLoader)
            logging.config.dictConfig(log_setting)
            logger.info("init logging end, from {}".format(LOGGING_CONFIG_FILE))
        except:
            logger.error(traceback.format_exc())
            logger.warning("read {} failure, init default logging...".format(LOGGING_CONFIG_FILE))
            use_default = True

    if use_default:
        logging.basicConfig(
            level=default_level,
            format=default_format
        )


_init_logging()


class ApplicationContext(object):
    app_config = dict()  # running active config
    messages = dict()
    application_name = None
    host = "127.0.0.1"
    port = "8080"
    active = None  # running active
    language = LanguageType.zh_TW.value
    mysql_client = None
    timezone = "Asia/Taipei"
    db_config = None
    s3_config = None

    def __init__(self):
        sstime = time.time()
        self.__load_active_profiles()
        if not self.app_config:
            raise EnvironmentError("active profile not found or can not load...")
        # error訊息
        self.__load_msg_property()
        # server 設定
        server_config = self.app_config["server"]
        self.context_path = server_config["contextPath"]
        self.host = server_config["host"]
        self.port = server_config["port"]

        root_config = self.app_config["eyesmedia"]
        self.api_version = root_config["api"]["version"]
        self.api_path_name = root_config["api"]["path-name"]
        # TimeZone
        timezone = root_config.get("localTimeZone")
        if timezone:
            self.timezone = timezone
        # 語系
        language = root_config.get("locale")
        if language:
            self.language = language
        # database
        self.db_config = root_config.get("database")
        if self.db_config:
            self.mysql_client = self.init_mysql_client(self.db_config.get("mysql-dc-governance"))
        # aws s3
        self.s3_config = S3ApplicationConfig(self.app_config).config

        costtiem = time.time() - sstime
        logger.info("application is initialized, cost {}/s".format(costtiem))

    def __load_active_profiles(self):
        # read bootstrap.yml
        with open(BOOTSTRAP_CONFIG_FILE, encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        self.application_name = data["application"]["name"]
        # multiple active profiles
        self.active = data["profiles"]["active"]
        # load cloud config
        cloud_config = data["cloud"]["config"]
        for active in self.active.split(','):
            yml_url = cloud_config["uri"] + "/" + active + "/" + self.application_name + "-" + active + ".yml"
            try:
                self.app_config.update(load_config(cloud_config, yml_url))
                logger.info("load cloud config file({}) success".format(yml_url))
            except:
                logger.warning("cloud config not found or loading fail, file path {}".format(yml_url, cloud_config))

        if not self.app_config:
            # load local config file
            with open(DEFAULT_CONFIG_FILE, encoding="utf-8") as stream:
                self.app_config.update(yaml.safe_load(stream))
            logger.info("load local config file({}) success".format(DEFAULT_CONFIG_FILE))

    def __load_msg_property(self):
        if os.path.exists(DEFAULT_MESSAGE_FILE):
            try:
                msg_prop = configparser.ConfigParser()
                msg_prop.read(DEFAULT_MESSAGE_FILE)
                for section in msg_prop.sections():
                    for key in msg_prop[section]:
                        self.messages.setdefault(key, msg_prop[section][key])
                logger.info("load messages.properties end, size is {}".format(len(self.messages)))
            except:
                logger.warning("load messages.properties failure... {}".format(traceback.format_exc()))

    def init_mongo_client(self, config):
        if not config:
            return None
        try:
            mongo_config = MongoConfig(host=config["host"],
                                       port=config.get("port"),
                                       dbname=config["dbname"],
                                       username=config["username"],
                                       password=str(config["pwd"]),
                                       replicaset=config.get("replica-set")
                                       )
            mongo_config.timezone = self.timezone
            mongo_config.auth_source = config.get("authentication-database")
            mongo_config.auth_mode = config.get("authentication-mode")

            provider = MongoClientProvider(mongo_config)
            logger.info("init MongoClient success, {}".format(config))
            return provider.create_client(connect=False,
                                          socketTimeoutMS=10000,
                                          maxIdleTimeMS=10000,
                                          connectTimeoutMS=10000,
                                          maxPoolSize=10)
        except:
            logger.error("init MongoDB Client has error, config is {}".format(config))
            raise

    def init_mysql_client(self, config):
        if not config:
            return None
        try:
            mysql_config = MySqlConfig(host=config["host"],
                                       port=config["port"],
                                       dbname=config["dbname"],
                                       username=config["username"],
                                       password=str(config["password"])
                                       )
            provider = MySqlConnectionProvider(mysql_config)
            logger.info("init mysql client success, {}".format(mysql_config))
            return provider
        except:
            logger.error("init mysql client has error, config is {}".format(config))
            raise

    def init_elasticsearch_client(self, config):
        if not config:
            return None
        try:
            cluster_nodes = config["cluster-nodes"].split(",")
            es = Elasticsearch(hosts=cluster_nodes,
                               timeout=5,
                               maxsize=200, block=True
                               # sniff_on_start=True,
                               # sniff_on_connection_fail=True,
                               # sniffer_timeout=config["timeout"]
                               )
            logger.info("init Elasticsearch client success, {}".format(es))
            return es
        except:
            logger.error("init Elasticsearch client has error, config is {}".format(config))
            raise


app_context = ApplicationContext()
