from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    name: str = Field(...)
    userid: str = Field(...)
    password: str = Field(...)
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
    total_work_time: dict = Field(...)
    this_mon_work_time: dict = Field(...)
    prev_mon_work_time: dict = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "홍길동",
                "userid": "gildong21",
                "password": "gildongpasswd21",
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
                        "start_date":"20210211", 
                        "end_date": "20210215", 
                        "description": "신병위로휴가"
                    }
                ],
                "total_work_time": "600",
                "this_mon_work_time": "35",
                "prev_mon_work_time": "60"
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    userid: Optional[str]
    password: Optional[str]
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
    total_work_time: Optional[dict]
    this_mon_work_time: Optional[dict]
    prev_mon_work_time: Optional[dict]

    class Config:
        schema_extra = {
            "example": {
                "name": "홍길동",
                "userid": "gildong21",
                "password": "gildongpasswd21",
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
                        "start_date":"20210211", 
                        "end_date": "20210215", 
                        "description": "신병위로휴가"
                    }
                ],
                "total_work_time": "600",
                "this_mon_work_time": "35",
                "prev_mon_work_time": "60"
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
