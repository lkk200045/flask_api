# -*- coding: utf-8 -*-
import logging
import repository
from entity.metric_catalog_tag import MetricCatalogTagEntity

logger = logging.getLogger("application")


class MetricCatalogTagDao(repository.MySQLRepository):
    """ 分類標籤 """

    def find_by_id(self, tag_id: str, connection=None) -> dict:
        sql = "SELECT * FROM metric_catalog_tag WHERE tag_id = %(tag_id)s"
        params = {
            "tag_id": tag_id
        }
        list = self.find(sql, params=params, connection=connection)
        return list[0] if list and len(list) > 0 else None

    def find_by_field_id(self, field_id: str, connection=None) -> MetricCatalogTagEntity:
        sql = "SELECT " \
              "metric_catalog_tag.*" \
              " FROM metric_field_catalog,metric_catalog_tag" \
              " WHERE metric_field_catalog.field_id = %(field_id)s" \
              " AND metric_field_catalog.catalog_tag_id = metric_catalog_tag.tag_id"
        params = {
            "field_id": field_id
        }
        list = self.find(sql, params=params, connection=connection)
        return MetricCatalogTagEntity(**list[0]) if list and len(list) > 0 else None
