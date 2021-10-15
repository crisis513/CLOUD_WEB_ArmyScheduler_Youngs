import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from .mongodb_helper import work_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.army_scheduler_db

works_collection = database.get_collection('Works')

async def retrieve_works():
    works = []
    async for work in works_collection.find():
        works.append(work_helper(work))
    return works


async def add_work(work_data: dict) -> dict:
    work = await works_collection.insert_one(work_data)
    new_work = await works_collection.find_one({"_id": work.inserted_id})
    return work_helper(new_work)


async def retrieve_work(id: int) -> dict:
    work = await works_collection.find_one({"work_id": id})
    if work:
        return work_helper(work)


async def delete_work(id: int):
    work = await works_collection.find_one({"work_id": id})
    if work:
        await works_collection.delete_one({"work_id": id})
        return True


async def update_work_data(id: int, data: dict):
    work = await works_collection.find_one({"work_id": id})
    if work:
        works_collection.update_one({"work_id": id}, {"$set": data})
        return True
