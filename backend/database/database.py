from time import time
from typing import Union
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient

from backend.Model.usermodel import User
from backend.errors.errormodel import Error
from backend.Model import usermodel
from backend.Model import channelmodel

from backend.database import utils

from config._secrets import _MONGO_URI


class Database:
    """
    A class to containing async methods to manage database operations
    ...

    Methods
    -------
    register_user(username: str, hash: str)
        Registers a user to the user collection in database
    """

    def __init__(self):
        self.db = AsyncIOMotorClient(_MONGO_URI).main

    async def register_user(
        self, username: str, hash: str
    ) -> Union[usermodel.User, Error]:
        collection = self.db.users
        try:
            user = usermodel.User(
                username=username,
                hash=hash,
                channels=[],
            )
            x = await collection.insert_one(user.dict(exclude={"id"}))
            user.id = str(x.inserted_id)
            return user
        except Exception as e:
            raise e

    async def create_channel(
        self, name: str, hash: str, owner: channelmodel.User
    ) -> Union[channelmodel.Channel, Error]:
        collection = self.db.channels
        created_at = int(time())
        try:
            channel = channelmodel.Channel(
                created_at=created_at, name=name, hash=hash, messages=[], users=[owner]
            )
            x = await collection.insert_one(channel.dict(exclude={"id"}))
            channel.id = str(x.inserted_id)
            return channel
        except Exception as e:
            return Error(message="Could not create channel", code=1)

    async def fetch_channel(self, id: str) -> Union[channelmodel.Channel, Error]:
        id = ObjectId(id)
        collection = self.db.channels
        channel = await collection.find_one({"_id": id})
        if not channel:
            return Error(message="Channel does not exist", code=404)
        else:
            return channelmodel.Channel(
                _id=str(channel["_id"]),
                created_at=channel["created_at"],
                name=channel["name"],
                hash=channel["hash"],
                messages=channel["messages"],
                users=channel["users"],
                meta=channel["meta"],
            )

    async def join_channel(self, user: usermodel.User, id: str) -> Union[None, Error]:
        channel = await self.fetch_channel(id)
        if isinstance(channel, Error):
            return channel
        channeluser = utils.um_to_cum(user)
        if channeluser.dict() in channel.users:
            return Error("User already in channel.", 1)
        else:
            collection = self.db.channels
            channel.users.append(channeluser)
            await collection.update_one(
                {"_id": ObjectId(channel.id)}, {"$set": channel.dict()}
            )
            collection = self.db.users
            userchannel = utils.cm_to_ucm(channel, int(time()))
            user.channels.append(userchannel)
            await collection.update_one(
                {"_id": ObjectId(user.id)}, {"$set": user.dict()}
            )

    async def update_channel(self, chID: str, **kwargs) -> Union[None, Error]:
        collection = self.db.channels
        channel = await self.get_channel(chID)
        for k, v in kwargs:
            await collection.replace_one(channel.dict(), {k: v})

    async def get_user(self, uID):
        collection = self.db.users
        user = await collection.find_one({"ID": uID})
        if not user:
            return Error(f"User does not exist", 404)
        else:
            return User(
                ID=user["ID"],
                username=user["username"],
                password=user["password"],
                direct_messages=user["direct_messages"],
            )
