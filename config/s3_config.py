# -*- coding: utf-8 -*-
import logging
from eyesmediapyutils.aws_s3 import S3Config

logger = logging.getLogger("application")


class S3ApplicationConfig(object):
    config = None

    def __init__(self, app_config):
        config = app_config.get("s3")
        if not config:
            return
        try:
            region = config.get("region")
            access_key = config["access-key"]
            secret_key = config["secret-key"]
            bucket_name = config["bucket-name"]
            self.config = S3Config(bucket_name, access_key, secret_key, region)
        except:
            logger.error("application include s3 config, must be setting access-key, secret-key, bucket-name...")
            raise
