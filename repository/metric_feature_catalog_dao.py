# -*- coding: utf-8 -*-
import logging
import repository

logger = logging.getLogger("application")


class MetricFeatureCatalogDao(repository.MySQLRepository):
    """ 特徵標籤與分類標籤關聯 """
