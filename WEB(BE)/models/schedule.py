from typing import Optional

from pydantic import BaseModel, Field


class ScheduleModel(BaseModel):
    consider_from_date: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "consider_from_date": "2021-01-01",
                "start_date": "2021-02-01",
                "end_date": "2021-03-01"
            }
        }

class UpdateScheduleModel(BaseModel):
    consider_from_date: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

    class Config:
        schema_extra = {
                "consider_from_date": "2021-01-01",
                "start_date": "2021-02-01",
                "end_date": "2021-03-01"
        }


def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
