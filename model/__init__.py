# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel
from eyesmediapyutils.datetime import DEFAULT_DATETIME_PATTERN


class BaseSupportModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        orm_mode = True


class BaseDateTimeFormatSupportModel(BaseSupportModel):
    class Config(BaseSupportModel.Config):
        json_encoders = {
            datetime: lambda v: v.strftime(DEFAULT_DATETIME_PATTERN)
        }
