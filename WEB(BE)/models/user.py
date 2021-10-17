from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    name: str = Field(...)
    user_id: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)
    is_admin: bool = Field(...)
    en_date: str = Field(...)
    de_date: str = Field(...)
    birth_date: str = Field(...)
    now_class: str = Field(...)
    unit_company: str = Field(...)
    unit_platoon: str = Field(...)
    unit_squad: str = Field(...)
    position: str = Field(...)
    work_list: list = Field(...)
    vacation: list = Field(...)
    total_worked_time: dict = Field(...)
    this_month_worked_time: dict = Field(...)
    this_month_work_time_left: dict = Field(...)
    prev_month_worked_time: dict = Field(...)
    prev_day_worktime: int = Field(...)
    prev_night_worktime: int = Field(...)
    prev_free_worktime: int = Field(...)
    new_day_worktime: int = Field(...)
    new_night_worktime: int = Field(...)
    new_free_worktime: int = Field(...)
    fatigue: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "홍길동",
                "user_id": "gildong21",
                "password": "gildongpasswd21",
                "email": "gildong@test.com",
                "is_admin": False,
                "en_date": "2020-11-09",
                "de_date": "2022-05-08",
                "birth_date": "1995-05-26",
                "now_class": "상병",
                "unit_company": "종합정비창",
                "unit_platoon": "본부소대",
                "unit_squad": "통신분대",
                "position": "군사과학기술병",
                "work_list": [ 1, 2 ],
                "vacation": [
                    {
                        "start_date": "2021-05-01",
                        "end_date": "2021-05-04",
                        "description": "신병위로휴가",
                    },
                    {
                        "start_date": "2021-08-04",
                        "end_date": "2021-08-10",
                        "description": "청원휴가",
                    }
                ],
                "total_worked_time": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "this_month_worked_time": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "this_month_work_time_left": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "prev_month_worked_time": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "prev_day_worktime": 0,
                "prev_night_worktime": 0,
                "prev_free_worktime": 0,
                "new_day_worktime": 0,
                "new_night_worktime": 0,
                "new_free_worktime": 0,
                "fatigue": 0
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    user_id: Optional[str]
    password: Optional[str]
    email: Optional[str]
    is_admin: Optional[bool]
    en_date: Optional[str]
    de_date: Optional[str]
    birth_date: Optional[str]
    now_class: Optional[str]
    unit_company: Optional[str]
    unit_platoon: Optional[str]
    unit_squad: Optional[str]
    position: Optional[str]
    work_list: Optional[list]
    vacation: Optional[list]
    total_worked_time: Optional[dict]
    this_month_worked_time: Optional[dict]
    this_month_work_time_left: Optional[dict]
    prev_month_worked_time: Optional[dict]
    prev_day_worktime: Optional[int]
    prev_night_worktime: Optional[int]
    prev_free_worktime: Optional[int]
    new_day_worktime: Optional[int]
    new_night_worktime: Optional[int]
    new_free_worktime: Optional[int]
    fatigue: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "name": "홍길동",
                "user_id": "gildong21",
                "password": "gildongpasswd21",
                "email": "gildong@test.com",
                "is_admin": False,
                "en_date": "2020-11-09",
                "de_date": "2022-05-08",
                "birth_date": "1995-05-26",
                "now_class": "상병",
                "unit_company": "종합정비창",
                "unit_platoon": "본부소대",
                "unit_squad": "통신분대",
                "position": "군사과학기술병",
                "work_list": [ 1, 2 ],
                "vacation": [
                    {
                        "start_date": "2021-05-01",
                        "end_date": "2021-05-04",
                        "description": "신병위로휴가",
                    },
                    {
                        "start_date": "2021-08-04",
                        "end_date": "2021-08-10",
                        "description": "청원휴가",
                    }
                ],
                "total_worked_time": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "this_month_worked_time": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "this_month_work_time_left": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "prev_month_worked_time": {
                    "day_worktime": 0,
                    "night_worktime": 0,
                    "free_worktime": 0
                },
                "prev_day_worktime": 0,
                "prev_night_worktime": 0,
                "prev_free_worktime": 0,
                "new_day_worktime": 0,
                "new_night_worktime": 0,
                "new_free_worktime": 0,
                "fatigue": 0
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
