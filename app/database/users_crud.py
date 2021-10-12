import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from .mongodb_helper import user_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.army_scheduler_db

users_collection = database.get_collection('Users')

async def retrieve_users():
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users


async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"userid": user.inserted_id})
    return user_helper(new_user)


async def retrieve_user(id: str) -> dict:
    user = await users_collection.find_one({"userid": ObjectId(id)})
    if user:
        return user_helper(user)


async def delete_user(id: str):
    user = await users_collection.find_one({"userid": ObjectId(id)})
    if user:
        await users_collection.delete_one({"userid": ObjectId(id)})
        return True


async def update_user_data(id: str, data: dict):
    user = await users_collection.find_one({"userid": id})
    if user:
        users_collection.update_one({"userid": id}, {"$set": data})
        return True
