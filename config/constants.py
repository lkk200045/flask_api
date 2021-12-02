# -*- coding: utf-8 -*-
from enum import Enum

# default global elasticsearch  constants
ES_SCROLL_SIZE = 20
ES_SCROLL_ALIVE = "1m"

# mongoDB auth mode
MONGODB_AUTH_MODE_SHA1 = "SCRAM-SHA-1"
MONGODB_AUTH_MODE_SHA256 = "SCRAM-SHA-256"


class LanguageType(Enum):
    zh_CN = "zh_CN"
    zh_TW = "zh_TW"
    en_US = "en_US"
