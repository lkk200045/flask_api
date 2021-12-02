# -*- coding: utf-8 -*-
import logging
import repository
from typing import List
from entity.system_params_config import SystemParamsConfigEntity

logger = logging.getLogger("application")


class SystemParamsConfigDao(repository.MySQLRepository):
    """ 系統常數 """

    def __find_by_condition(
            self, group_code: str = None, config_codes: List[str] = None, is_disabled: int = None, config_parent_code: str = None, connection=None
    ) -> List[SystemParamsConfigEntity]:
        """
        依據條件查詢

        Args:
            group_code: 群組代碼，小寫顯示
            config_codes: 系統常數代碼
            is_disabled: 是否停用
            config_parent_code: 上層代碼
            connection: 資料庫連線物件

        Returns:
            List of SystemParamsConfigEntity
        """
        sql = "SELECT config_id,config_code,config_name,config_parent_code,is_disabled" \
              " FROM system_params_config" \
              " WHERE 1=1"
        params = dict()
        # 群組代碼
        if group_code and len(group_code) > 0:
            sql += " AND group_code = %(group_code)s"
            params.setdefault("group_code", group_code.lower())
        #  上層代碼
        if config_parent_code and len(config_parent_code) > 0:
            sql += " AND config_parent_code = %(config_parent_code)s"
            params.setdefault("config_parent_code", config_parent_code)
        # 常數代碼
        if config_codes and len(config_codes) > 0:
            is_multi_config = len(config_codes) > 1
            sql += " AND config_code {} %(config_codes)s".format("in" if is_multi_config else "=")
            params.setdefault("config_codes", config_codes if is_multi_config else config_codes[0])
        # 是否停用
        if is_disabled is not None and -1 < is_disabled < 2:
            sql += " AND is_disabled = %(is_disabled)s"
            params.setdefault("is_disabled", is_disabled)
        # 排序
        sql += " ORDER BY config_code ASC"
        datas = self.find(sql, params=params, connection=connection)
        return [SystemParamsConfigEntity(**data) for data in datas]

    def find_by_group_code(
            self, group_code: str, config_codes: List[str] = None, is_disabled: int = None, connection=None
    ) -> List[SystemParamsConfigEntity]:
        """ 依據群組編號查詢 """
        return self.__find_by_condition(group_code=group_code,
                                        config_codes=config_codes,
                                        is_disabled=is_disabled,
                                        connection=connection
                                        )

    def find_by_id(self, config_id: str, connection=None) -> SystemParamsConfigEntity:
        datas = self.find_by_ids(config_ids=[config_id], connection=connection)
        return datas[0] if datas and len(datas) > 0 else None

    def find_by_ids(self, config_ids: List[str], connection=None) -> List[SystemParamsConfigEntity]:
        if config_ids is None or len(config_ids) == 0:
            return list()
        is_multiple = len(config_ids) > 1
        sql = "SELECT * FROM system_params_config WHERE config_id {} %(config_ids)s".format("in" if is_multiple else "=")
        params = {
            "config_ids": config_ids if is_multiple else config_ids[0]
        }
        sql += " ORDER BY config_code ASC"
        datas = self.find(sql, params=params, connection=connection)
        return [SystemParamsConfigEntity(**data) for data in datas]

    def find_by_parent_code(self, config_parent_code: str, is_disabled: int = None, connection=None) -> List[SystemParamsConfigEntity]:
        return self.__find_by_condition(config_parent_code=config_parent_code, is_disabled=is_disabled, connection=connection)

    def find_config_child_table(self, config_parent_code: str, group_code: str, connection=None) -> List[SystemParamsConfigEntity]:
        return self.__find_by_condition(group_code=group_code, config_parent_code=config_parent_code, connection=connection)
