from time import time

from backend.Model import channelmodel
from backend.Model import usermodel

def um_to_cum(user: usermodel.User, admin: bool = False):
    return channelmodel.User(id=user.id, username=user.username, admin=admin, meta=user.meta)

def cm_to_ucm(channel: channelmodel.Channel, joined_at: int):
    return usermodel.Channel(id=channel.id, name=channel.name, public=False, joined_at=joined_at, meta=channel.meta)
