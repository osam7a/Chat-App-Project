import uuid
from datetime import datetime

from fastapi import Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from paseto.exceptions import PasetoException

from . import auth_utils
from .auth_utils import OAuth2PasswordBearerWithCookie

from fastapi import APIRouter

from web.database import asyncdb

from web.Models import userModel
from web.Models.userModel import User
from web.Models import tokenModel

try:
    from config import test_config as config
except:
    from config import config

import bot

token_arr = []


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")
router = APIRouter()

@router.post('/register')
async def register(user: userModel.RegisterUser):
    try:
        discord_user = await bot.client.fetch_user(user.uid)
    except:
        return {"status": "Invalid Discord User ID"}
    token = str(uuid.uuid4())
    if user.password != '':
        hashed_pass = auth_utils.get_password_hash(user.password)
    else:
        return {"status": "Invalid credentials"}
    if user.username != '':
        token_arr.append((token, datetime.now(), user.uid,
                         user.username, hashed_pass))
    else:
        return {"status": "Invalid credentials"}
    await discord_user.send(
        "**IMPORTANT**\n"
        "To complete the registration process, please enter the token provided below to the rediredted page. The token **expires in 5 minutes**.\n\n"
        f"This message is sent to you because your discord user ID was used under the username **{user.username}** for the book santa discord server account registration process.\n"
        "If it was not done by you, sit back and relax, nothing to be worried about and **DO NOT** give this token to anyone else, it might be an attempt to register a fake account or a typing mistake.\n")
    await discord_user.send(f"`{token}`")
    return {"status": "success"}


@router.post('/verify-token')
async def verify(token: tokenModel.Token):
    for tokens in token_arr:
        if token.token == tokens[0]:
            token_arr.remove(tokens)
            time_diff = datetime.now() - tokens[1]
            if time_diff.total_seconds() < 300:
                await asyncdb.add_user(uid=tokens[2], username=tokens[3], hash=tokens[4], meta=asyncdb.generateJson({"content": {}}))
                return {"status": "success"}
            else:
                return {"status": "Token has expired"}
    return {"status": "Token is invalid"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_utils.decode_access_token(token)
        data = payload['message']['sub']
        if data is None:
            raise credentials_exception
        token_data = tokenModel.PasetoTokenData(
            uid=data['uid'], username=data['username'])
    except PasetoException:
        raise credentials_exception
    return userModel.User(uid=token_data.uid, username=token_data.username)


@router.post('/token')
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_utils.authenticate_user(uid=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_utils.create_access_token(
        {"sub": {"uid": user.uid, "username": user.username}})
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return


@router.get('/logout')
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie("access_token")
    return


@router.get('/me')
async def my_user(current_user: User = Depends(get_current_user)):
    return current_user
