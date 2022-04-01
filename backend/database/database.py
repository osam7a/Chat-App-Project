
from motor.motor_asyncio import AsyncIOMotorClient
from config._secrets import _MONGO_URI

class Database:
    def __init__(self):
        self.db = AsyncIOMotorClient(_MONGO_URI)

    async def get_channel(self, chID):
        collection = self.db.channels

    async def create_channel(self, chName, chPassword):
        collection = self.db.channels

    async def update_channel(self, chID, **kwargs):
        collection = self.db.channels

    async def register_user(self, username, password):
        collection = self.db.users

    async def update_user(self, userID):
        collection = self.db.users