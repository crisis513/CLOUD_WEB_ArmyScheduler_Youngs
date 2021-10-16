from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from models.schedule import *
from algorithm.schedule import *

router = APIRouter()


@router.post("/", response_description="schedule data added")
async def add_schedule_data(schedule: ScheduleModel = Body(...)):
    sch = Scheduler(schedule.consider_from_date, schedule.start_date, schedule.end_date)
    sch.schedule()
    return ResponseModel(f"근무 {len(sch.result_event_list)}개 생성 완료", "schedule added successfully.")
