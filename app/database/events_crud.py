import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from .mongodb_helper import event_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.army_scheduler_db

events_collection = database.get_collection('Events')

async def retrieve_events():
    events = []
    async for event in events_collection.find():
        events.append(event_helper(event))
    return events


async def add_event(event_data: dict) -> dict:
    event = await events_collection.insert_one(event_data)
    new_event = await events_collection.find_one({"event_id": event.inserted_id})
    return event_helper(new_event)


async def retrieve_event(id: str) -> dict:
    event = await events_collection.find_one({"event_id": ObjectId(id)})
    if event:
        return event_helper(event)


async def delete_event(id: str):
    event = await events_collection.find_one({"event_id": ObjectId(id)})
    if event:
        await events_collection.delete_one({"event_id": ObjectId(id)})
        return True


async def update_event_data(id: str, data: dict):
    event = await events_collection.find_one({"event_id": id})
    if event:
        events_collection.update_one({"event_id": id}, {"$set": data})
        return True