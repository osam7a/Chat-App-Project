from pymongo import MongoClient
from _dataclasses.message import Message
from _dataclasses.user import User
from _dataclasses.channel import Channel
from _dataclasses.error import Error
import datetime
import paseto
import secrets
import uuid

class Database:
    def __init__(self):
        self.conn = MongoClient("mongodb+srv://osam7a:Gh6wr52gi5@chatapp.rz0eb.mongodb.net/Main?retryWrites=true&w=majority")
        self.db = self.conn['Main']

    def createChannel(self, chName, chPassword):
        col = self.db['channels']
        f = [i for i in col.find({"chName": chName})]
        if len(f) == 0:
            col.insert_one(Channel(
                chName = chName,
                chPassword = chPassword,
                users = [],
                messages = []
            ).to_dict)
        else: 
            return Error(f"Channel with name {chName} already exists")

    def getChannel(self, chName):
        col = self.db['channels']
        f = [i for i in col.find({"chName": chName})]
        if len(f) == 0:
            return Error(f"No channel with name {chName} found")
        else: 
            f2 = col.find_one({"chName": chName})
            return Channel(
                chName = f2['chName'],
                chPassword = f2['chPassword'],
                users = f2['users'],
                messages = f2['messages']
            )

    def joinChannel(self, chName, chPassword, user):
        col = self.db['channels']
        f = [i for i in col.find({"chName": chName})]
        if len(f) == 0:
            return Error(f"No channel with name {chName} found")
        else:
            f2 = col.find_one({"chName": chName})
            if f2['chPassword'] == chPassword:
                if user in f['users']:
                    return Error(f"user {user['username']} is already in the channel")
                users = f['users']
                users.append(user)
                col.update_one({"chName": chName}, {"$set": {"users": users}})
            else:
                return Error(f"Incorrect password for channel {chName}")

    def send_message(self, chName, username, message):
        col = self.db['channels']
        f = [i for i in col.find({"chName": chName})]
        if len(f) == 0:
            return Error(f"No channel with name {chName} found")
        else:
            f = col.find_one({"chName": chName})
            if username not in f['users']:
                return Error(f"{username} is not allowed to send a message to {chName}")
            msgsUpdated = f['messages']
            msgsUpdated.append(Message(
                author = username,
                content = message,
                created_at = datetime.datetime.utcnow()
            ).to_dict)
            col.update_one({"chName": chName}, {"$set": {"messages": msgsUpdated}})


    def registerUser(self, username, password):
        col = self.db['users']
        key = secrets.token_bytes(32)
        uID = uuid.uuid4()
        data = {
            "id": uID
            "username": username,
            "password": password
        }
        auth = paseto.create(key=key, purpose='local', claims = data).decode('utf-8')
        f = [i for i in col.find({"username": username, "id": uID})]
        if len(f) == 0:
            
            col.insert_one(User(
                id = uID
                username = username,
                password = passW,
                authorization = auth
            ).to_dict)
        else:
            return Error("Already registered.")

    def authorize(self, token):
        pass

    def getUser(self, username):
        pass

if __name__ == "__main__":
    a = Database().createChannel("Test Channel", "123456789")
    if isinstance(a, Error):
        print(a.message)
    a2 = Database().send_message("Test Channel", User(
        username = "osam7a",
        password = "7pq4HC2k09"
    ).to_dict, "test message")
    if isinstance(a2, Error):
        print(a2.message)
    print(Database().getChannel("Test Channel").messages)
    