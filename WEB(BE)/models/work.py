from typing import Optional

from pydantic import BaseModel, Field


class WorkModel(BaseModel):
    work_id: int = Field(...)
    work_name: str = Field(...)
    work_setting: list = Field(...)
    worker_list: list = Field(...)
    work_option1: int = Field(...)
    work_option2: int = Field(...)
    work_option3: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "work_id": 1,
                "work_name": "CCTV",
                "worker_list": ["u10", "u11"],
                "work_setting": {
                    "start_time": "04:00",
                    "end_time": "10:00",
                    "num_workers": 3,
                },
                "work_option1": 0,
                "work_option2": 1,
                "work_option3": 2,
            }
        }


class UpdateWorkModel(BaseModel):
    work_id: Optional[int]
    work_name: Optional[str]
    work_setting: Optional[list]
    worker_list: Optional[list]
    work_option1: Optional[int]
    work_option2: Optional[int]
    work_option3: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "work_id": 1,
                "work_name": "CCTV",
                "worker_list": ["u10", "u11"],
                "work_setting": [{
                    "start_time": "04:00",
                    "end_time": "10:00",
                    "num_workers": 3,
                }],
                "work_option1": 0,
                "work_option2": 1,
                "work_option3": 2,
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
