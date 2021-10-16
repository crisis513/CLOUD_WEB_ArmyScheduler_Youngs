from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.events_crud import *
from models.event import *

router = APIRouter()

@router.get("/", response_description="events retrieved")
async def get_events():
    events = await retrieve_events()
    return ResponseModel(events, "events data retrieved successfully") \
        if len(events) > 0 \
        else ResponseModel(
        events, "Empty list returned")


@router.get("/{id}", response_description="event data retrieved")
async def get_event_data(id):
    event = await retrieve_event(id)
    return ResponseModel(event, "event data retrieved successfully") \
        if event \
        else ErrorResponseModel("An error occured.", 404, "event doesn't exist.")


@router.post("/", response_description="event data added into the database")
async def add_event_data(event: EventModel = Body(...)):
    event = jsonable_encoder(event)
    new_event = await add_event(event)
    return ResponseModel(new_event, "event added successfully.")


@router.delete("/{id}", response_description="event data deleted from the database")
async def delete_event_data(id: int):
    deleted_event = await delete_event(id)
    return ResponseModel("event with ID: {} removed".format(id), "event deleted successfully") \
        if deleted_event \
        else ErrorResponseModel("An error occured", 404, "event with id {0} doesn't exist".format(id))


@router.put("/{id}")
async def update_event(id: int, req: UpdateEventModel = Body(...)):
    updated_event = await update_event_data(id, req.dict())
    return ResponseModel("event with ID: {} name update is successful".format(id),
                         "event name updated successfully") \
        if updated_event \
        else ErrorResponseModel("An error occurred", 404, "There was an error updating the event.".format(id))
