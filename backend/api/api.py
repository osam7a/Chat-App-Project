from fastapi import FastAPI, Header
from backend.database.database import Database
from backend.Model.channelmodel import Channel
from backend.Model.usermodel import User
from backend.errors.errormodel import Error

app = FastAPI()

async def authorize(auth):
    pass

async def get_code_string(code: str): 
    f = open("errorcodes.txt", "r")
    lines = f.readlines()
    for i in lines:
        if i.startswith(str(code)): 
            return i.split()[1:]

@app.get("/")
async def main():
    return {
        "Endpoints": [{
            "/fetch_channel": """
                Description: Returns a dict of channel object
                Returns: dict of Channel object or Error
                Parameters: 
                    id: string, ID of channel
                """,
            "/create_channel": """
                Description: Creates a channel with specified properties
                Returns: The channel created
                Parameters: 
                    name: string, name of the channel
                    hash: string, i dont know what's this lol
                    auth: Header, authentication token
                """
        }]
    }

@app.get("/fetch_channel")
async def fetch_channel(id: str) -> dict:
    db = Database()
    channel = await db.fetch_channel(id)
    if not isinstance(channel, Error) and isinstance(channel, Channel):
        return channel.dict()
    else:
        return {
            "error": {
                "message": channel.message,
                "code": channel.code,
                "code_string": await get_code_string(channel.code)
            }
        }

@app.post("/create_channel", status_code=201)
async def create_channel(name: str, hash: str, Authorization = Header(None)) -> dict:
    db = Database()
    authorized = await authorize(Authorization)
    if authorized:
        channel = await db.create_channel(name, hash)
        if not isinstance(channel, Error) and isinstance(channel, Channel):
            return channel.dict()
        else:
            return {
                "error": {
                    "message": channel.message,
                    "code": channel.code,
                    "code_string": await get_code_string(channel.code)
                }
            }
    else:
        return {
            "error": {
                "message": "Authorization invalid",
                "code": 403,
                "code_string": await get_code_string(403)
            }
        }

@app.get("/fetch_user")
async def fetch_user(userID: str) -> dict:
    db = Database()
    user = await db.fetch_user(userID)
    if isinstance(user, Error) and not isinstance(user, User):
        return {
            "error": {
                "message": user.message,
                "code": user.code,
                "code_string": await get_code_string(user.code)
            }
        }
    else:
        return user.dict()

@app.post("/register_user", status_code=201)
async def register_user(username: str, hash: str, Authorization = Header(None)) -> dict:
    db = Database()
    user = await db.register_user(username, hash)
    authorized = await authorize(Authorization)
    if authorized:
        if not isinstance(user, Error) and isinstance(user, Channel):
            return user.dict()
        else:
            return {
                "error": {
                    "message": user.message,
                    "code": user.code,
                    "code_string": await get_code_string(user.code)
                }
            }
    else:
        return {
            "error": {
                "message": "Authorization invalid",
                "code": 403,
                "code_string": await get_code_string(403)
            }
        }