from passlib.context import CryptContext

from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.status import HTTP_401_UNAUTHORIZED

import paseto
from paseto.keys.symmetric_key import SymmetricKey
from paseto.protocols.v4 import ProtocolVersion4

from web.Models import userModel

try:
    from config import test_config as config
except:
    from config import config

from web.database import asyncdb


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(password_text, hashed_password):
    return pwd_context.verify(password_text, hashed_password)


async def get_user(uid: int):
    user = await asyncdb.get_user_from_db(uid)
    if user is None:
        return None
    return userModel.User(uid=user['uid'], username=user['username'])


async def authenticate_user(uid: int, password: str):
    user = await get_user(uid)
    if user is None:
        return False
    hashed_pass = await asyncdb.get_password(uid)
    if not verify_password(password, hashed_pass['hash']):
        return False
    return user


ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
PASETO_SECRET_KEY = SymmetricKey.generate(protocol=ProtocolVersion4)
def create_access_token(data: dict):
    return paseto.create(
        key=PASETO_SECRET_KEY,
        purpose='local',
        claims=data,
        exp_seconds=ACCESS_TOKEN_EXPIRE_MINUTES*60
    )


def decode_access_token(token):
    return paseto.parse(
        key=PASETO_SECRET_KEY,
        purpose='local',
        token=token,
    )
