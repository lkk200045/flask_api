# -*- coding: utf-8 -*-
import logging
from typing import Optional, Union
from uuid import UUID
from pydantic import Field
from model import BaseSupportModel

logger = logging.getLogger("application")


class GenericConstantAutocompleteReqModel(BaseSupportModel):
    """ 共用元件(下拉式選單/autocomplete) request model """
    text: Optional[str] = None


class GenericConstantAutocompleteResModel(BaseSupportModel):
    """ 共用元件(下拉式選單/autocomplete) response model """
    id: Union[UUID, str]  # 編號或代碼
    name: str
    alias_name: Optional[str] = Field(None, alias="aliasName")
    is_disabled: Optional[bool] = Field(False, alias="isDisabled")
    storage_type: Optional[str] = Field(None, alias="storageTypeCode")
