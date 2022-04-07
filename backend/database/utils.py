from time import time
from bson.objectid import ObjectId

from backend.Model import channelmodel
from backend.Model import usermodel


def um_to_cum(user: usermodel.User, admin: bool = False) -> channelmodel.User:
    return channelmodel.User(
        id=user.id, username=user.username, admin=admin, meta=user.meta
    )


def cm_to_ucm(channel: channelmodel.Channel, joined_at: int) -> usermodel.Channel:
    return usermodel.Channel(
        id=channel.id,
        name=channel.name,
        public=False,
        joined_at=joined_at,
        meta=channel.meta,
    )


def str_to_cmm(content: str, author: channelmodel.User) -> channelmodel.Message:
    id = str(ObjectId())
    created_at = int(time())
    return channelmodel.Message(id=id, created_at=created_at, author=author, content=content)