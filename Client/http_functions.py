import aiohttp
from Client.Model.usermodel import Channel
from Client.constants import BASE_URL

async def fetch_user(id):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"{BASE_URL}/user/fetch?id={id}") as resp:
            _json = resp.json()
            if "error" in _json:
                if _json['error']['code'] == 404:
                    return 404
            else:
                return User(
                    id = _json['id'],
                    username = _json['username'],
                    hash = _json['hash'],
                    channels = _json['channels'],
                    meta = _json['meta']
                )

async def fetch_channel(id):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"{BASE_URL}/channel/fetch?id={id}") as resp:
            _json = resp.json()
            if "error" in _json:
                if _json['error']['code'] == 404:
                    return 404
            else:
                return Channel(
                    id = _json['id'],
                    created_at = _json['created_at'],
                    name = _json['name'],
                    hash = _json['hash'],
                    messages = _json['messages'],
                    users = _json['users'],
                    meta = _json['meta']
                ) 

async def create_channel(name, hash):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"{BASE_URL}/channel/fetch?id={id}") as resp:
            _json = resp.json()
            if "error" in _json:
                # Error occured 
                if _json['error']['code'] == 1:
                    return 1
                else:
                    return Channel(
                        id = _json['id'],
                        created_at = _json['created_at'],
                        name = _json['name'],
                        hash = _json['hash'],
                        messages = _json['messages'],
                        users = _json['users'],
                        meta = _json['meta']
                    ) 

async def send_message(channel_id, message):
    pass

async def register_user(name, hash):
    pass

async def login_as(name, password):
    pass