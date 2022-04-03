from datetime import datetime
from time import time
from typing import Union
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient

from backend.Model.usermodel import User
from backend.errors.errormodel import Error
from backend.Model import usermodel
from backend.Model import channelmodel
from backend.Model.messagemodel import Message

_MONGO_URI = None

class Database:
    def __init__(self):
        self.db = AsyncIOMotorClient(_MONGO_URI).Main

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
            pass

    async def create_channel(
        self, name: str, hash: str, owner: channelmodel.User
    ) -> Union[channelmodel.Channel, Error]:
        collection = self.db.channels
        ch = collection.find_one({"name": name, "hash": hash})
        if ch:
            return Error(message="Already exists", code=1)
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

    async def join_channel(self, user: User, chID: str) -> Union[None, Error]:
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

<<<<<<< HEAD
    async def update_user(self, userID):
=======
    async def register_user(self, username: str, password: str):
        collection = self.db.users
        user = await collection.find_one({"username": username})
        if not user:
            user = User(
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
            x = await collection.insert_one(user)
            user.id = x.inserted_id
        else:
            return Error(message="User already registered", code=1)

    async def update_user(self, userID: str, **kwargs):
>>>>>>> 73ffbc84e76981e55a823e37f80b6a7cb52f9ac3
        collection = self.db.users
        user = await self.get_user(userID)
        for k, v in kwargs:
            await collection.replace_one(user.dict(), {k: v})

