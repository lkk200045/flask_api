import logging
from typing import Union,Set,Dict,List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field
from model import BaseSupportModel
from datetime import datetime
from eyesmediapyutils.datetime import DEFAULT_DATETIME_PATTERN


class ProviderAccountResModal(BaseSupportModel):
    account_id: Optional[str] = Field(alias="accountId")
    account_name: Optional[str] = Field(alias="accountName")

    class Config(BaseSupportModel.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(DEFAULT_DATETIME_PATTERN)
        }