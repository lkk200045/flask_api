import logging
from typing import Union,Set,Dict,List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field
from model import BaseSupportModel
from datetime import datetime
from eyesmediapyutils.datetime import DEFAULT_DATETIME_PATTERN

logger = logging.getLogger("application")

class connectInfoModel(BaseModel):
    account:Optional[str]
    pwd:Optional[str]
    host:Optional[str]
    port:Optional[str]
    url:Optional[str]

class connectInfoResModal(BaseSupportModel):
    account: Optional[str] = Field(alias="account")
    pwd: Optional[str] = Field(alias="pwd")
    host: Optional[str] = Field(alias="host")
    port: Optional[str] = Field(False, alias="port")
    url: Optional[str] = Field(False, alias="url")
   
    class Config(BaseSupportModel.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(DEFAULT_DATETIME_PATTERN)
        }