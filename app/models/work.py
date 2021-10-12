from typing import Optional

from pydantic import BaseModel, Field


class WorkModel(BaseModel):
    work_id: int = Field(...)
    work_name: str = Field(...)
    work_setting: dict = Field(...)
    work_option1: str = Field(...)
    work_option2: str = Field(...)
    work_option3: str = Field(...)
    work_period: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "work_id": 1,
                "work_name": "CCTV",
                "work_setting": {
                    "start_time": "04:00",
                    "end_time": "10:00",
                    "num_workers": 3,
                },
                "work_option1": "work_option1",
                "work_option2": "work_option2",
                "work_option3": "work_option3",
                "work_period": "work_period"
            }
        }


class UpdateWorkModel(BaseModel):
    work_id: Optional[int]
    work_name: Optional[str]
    work_setting: Optional[dict]
    work_option1: Optional[str]
    work_option2: Optional[str]
    work_option3: Optional[str]
    work_period: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "work_id": 1,
                "work_name": "CCTV",
                "work_setting": {
                    "start_time": "04:00",
                    "end_time": "10:00",
                    "num_workers": 3,
                },
                "work_option1": "work_option1",
                "work_option2": "work_option2",
                "work_option3": "work_option3",
                "work_period": "work_period"
            }
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
