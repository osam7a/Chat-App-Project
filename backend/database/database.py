import uuid
import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from config._secrets import _MONGO_URI
from Model.usermodel import User
from Model.errormodel import Error
from Model.channelmodel import Channel
from Model.messagemodel import Message

class Database:
    def __init__(self):
        self.db = AsyncIOMotorClient(_MONGO_URI)
        self.chatAppUser = User(
            ID = 00000,
            username = "Chat App",
            password = "00000",
            created_at = datetime.utcnow(),
            direct_messages = None
                                ).dict()

    async def get_channel(self, chID: int) -> Union[Channel, Error]:
        collection = self.db.channels
        channel = await collection.find_one({"ID": chID})
        if not channel:
            return Error(f"Channel does not exist", 404)
        else:
            return Channel(
                ID = channel["ID"],
                chName = channel["chName"],
                chPassword = channel["chPassword"],
                messages = channel["messages"],
                users = channel["users"]
            )

    async def create_channel(self, chName: str, chPassword: str) -> Union[None, Error]:
        collection = self.db.channels
        channelExists = await collection.find_one({"chName": chName})
        if not channel:
            chID = None
            await collection.insert_one(Channel(
                ID = chID,
                chName = chName,
                chPassword = chPassword,
                messages = [Message(
                    author = User(ID = 00000, username = "Admin", password = "00000", direct_messages = []).dict(),
                    content = f"Channel created at {datetime.datetime.utcnow().strftime('%c')} (UTC)"
                ).dict()],
                users = []
            ).dict())
        else:
            return Error(f"Channel already exists", 1)
            
    async def join_channel(self, user: User, chID: int) -> Union[None, Error]:
        collection = self.db.channels
        channel = await self.get_channel(chID)
        if user.dict() in channel.users:
            return Error("User already in channel.", 1)
        else:
            newUsers = channel.users
            newUsers.append(user.dict())
            newMessages = channel.messages
            newMessages.append(Message(
                author = user,
                content = f"{user.username} just joined!",
                created_at = datetime.utcnow
            ).dict())
            await self.update_channel(chID, users = newUsers, messages = newMessages)

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
                ID = user["ID"],
                username = user["username"],
                password = user["password"],
                direct_messages = user["direct_messages"]
            )

    async def register_user(self, username, password):
        collection = self.db.users
        user = await collection.find_one({"username": username})
        if not user:
            uID = None
            await collection.insert_one(User(
                ID = uID,
                username = username,
                password = password,
                created_at = datetime.utcnow(),
                direct_messages = [
                    {
                        "user": self.chatAppUser,
                        "messages": [
                            Message(
                                author = self.chatAppUser.dict(),
                                content = "Welcome to chatapp!, if you need help, contact us on discord osam7a#1017 or midnightFirefly#9122",
                                created_at = datetime.utcnow()
                            ).dict()
                        ]
                    }
                ]
            ).dict())

    async def update_user(self, userID):
        collection = self.db.users
        user = await self.get_user(chID)
        for k, v in kwargs:
            await collection.replace_one(user.dict(), {k: v})
