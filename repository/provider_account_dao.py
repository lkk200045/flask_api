# -*- coding: utf-8 -*-
import logging
import repository
from typing import List
from entity.provider_account import ProviderAccountEntity

logger = logging.getLogger("application")


class ProviderAccountDao(repository.MySQLRepository):
    """ 企業資料 """

    def find_account_id_by_name_like(self, account_name: str = None, connection=None) -> List[ProviderAccountEntity]:
        sql = "SELECT account_id,account_name FROM provider_account" \
              " WHERE 1=1"
        params = dict()
        if account_name and len(account_name) > 0:
            sql += " AND account_name like %(account_name)s"
            params.setdefault("account_name", "%{}%".format(account_name))
        sql += " ORDER BY account_name ASC"
        datas = self.find(sql, params=params, connection=connection)
        return [ProviderAccountEntity(**data) for data in datas]
