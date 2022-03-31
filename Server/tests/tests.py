import paseto
import uuid

key = secrets.token_bytes(32)
uID = uuid.uuid4()
data = {
    "id": uID,
    "username": 'osam7a',
    "password": 'password'
}
auth = paseto.create(key=key, purpose='local', claims = data).decode('utf-8')