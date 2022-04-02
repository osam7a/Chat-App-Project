from datetime import datetime
from time import time
from typing import Union
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient

from backend.Model.usermodel import User
from backend.errors.errormodel import Error
from backend.Model.channelmodel import Channel
from backend.Model.messagemodel import Message

from config._secrets import _MONGO_URI


class Database:
    def __init__(self):
        self.db = AsyncIOMotorClient(_MONGO_URI).main

    async def create_channel(self, name: str, hash: str) -> Union[Channel, Error]:
        collection = self.db.channels
        created_at = int(time())
        try:
            channel = Channel(
                created_at=created_at, name=name, hash=hash, messages=[], users=[]
            )
            x = await collection.insert_one(channel.dict(exclude={'id'}))
            channel.id = str(x.inserted_id)
            return channel
        except Exception as e:
            return Error(message="Could not create channel", code=1)

    async def fetch_channel(self, id: str) -> Union[Channel, Error]:
        id = ObjectId(id)
        collection = self.db.channels
        channel = await collection.find_one({"_id": id})
        if not channel:
            return Error(message="Channel does not exist", code=404)
        else:
            return Channel(
                _id=str(channel["_id"]),
                created_at=channel["created_at"],
                name=channel["name"],
                hash=channel["hash"],
                messages=channel["messages"],
                users=channel["users"],
                meta=channel["meta"],
            )

    async def join_channel(self, user: User, chID: int) -> Union[None, Error]:
        channel = await self.fetch_channel(chID)
        if user.dict() in channel.users:
            return Error("User already in channel.", 1)
        else:
            newUsers = channel.users
            newUsers.append(user.dict())
            newMessages = channel.messages
            newMessages.append(
                Message(
                    author=user,
                    content=f"{user.username} just joined!",
                    created_at=datetime.utcnow,
                ).dict()
            )
            await self.update_channel(chID, users=newUsers, messages=newMessages)

    async def update_channel(self, chID, **kwargs) -> Union[None, Error]:
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

    async def register_user(self, username, password):
        collection = self.db.users
        user = await collection.find_one({"username": username})
        if not user:
            uID = None
            await collection.insert_one(
                User(
                    ID=uID,
                    username=username,
                    password=password,
                    created_at=datetime.utcnow(),
                    direct_messages=[
                        {
                            "user": self.chatAppUser,
                            "messages": [
                                Message(
                                    author=self.chatAppUser.dict(),
                                    content="Welcome to chatapp!, if you need help, contact us on discord osam7a#1017 or midnightFirefly#9122",
                                    created_at=datetime.utcnow(),
                                ).dict()
                            ],
                        }
                    ],
                ).dict()
            )

    async def update_user(self, userID):
        collection = self.db.users
        user = await self.get_user(userID)
        for k, v in kwargs:
            await collection.replace_one(user.dict(), {k: v})
