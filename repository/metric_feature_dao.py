# -*- coding: utf-8 -*-
import logging
import repository
import uuid as uid
from typing import List
from entity.metric_feature import MetricFeatureEntity

logger = logging.getLogger("application")


class MetricFeatureDao(repository.MySQLRepository):
    """ 特徵標籤 """

    def find_by_field_id(self, field_id: str, connection=None) -> List[MetricFeatureEntity]:
        sql = "SELECT " \
              "metric_feature.*" \
              " FROM metric_field_feature, metric_feature" \
              " WHERE metric_field_feature.field_id = %(field_id)s" \
              " AND metric_field_feature.feature_id = metric_feature.feature_id"
        params = {
            "field_id": field_id
        }
        list = self.find(sql, params=params, connection=connection)
        return [MetricFeatureEntity(**data) for data in list]

    def insert_metric_feature(self, user_id: str, user_name: str, feature_label: str, feature_value: str, connection):
        feature_id = str(uid.uuid4())
        sql = "INSERT INTO metric_feature \
                value (%(feature_id)s\
                ,%(feature_label)s\
                ,%(feature_value)s\
                ,%(is_disabled)s\
                ,%(crt_user_id)s\
                ,%(crt_user_name)s\
                ,now()\
                ,%(mdy_user_id)s\
                ,%(mdy_user_name)s\
                ,now())"

        params = {
            "feature_id": feature_id,
            "feature_label": feature_label,
            "feature_value": feature_value,
            "is_disabled": 0,
            "crt_user_id": user_id,
            "crt_user_name": user_name,
            "mdy_user_id": user_id,
            "mdy_user_name": user_name
        }
        with connection.cursor() as cursor:
            cursor.execute(sql, args=params)
        return feature_id
