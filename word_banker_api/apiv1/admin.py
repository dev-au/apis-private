import json
import time

from fastapi import APIRouter, status
from pydantic import BaseModel
from data.word_get import word_options
from api_versions import api_v1
from data.coder import get_api_limit, generate_api
from data.database import session, engine
from data.models import Word, Key
from data.example import example_answer
from fastapi.exceptions import HTTPException
import requests

admin_router = APIRouter(prefix='/admin')
session = session(bind=engine)


@admin_router.get("/get-user-limit/{api_key}", tags=["Get user limit"])
async def get_limit(api_key: str):
    try:
        api_limit = get_api_limit(api_key)
        db_api = session.query(Key).filter(Key.api_key == api_key).first()
        now_limit = db_api.api_limit
        if db_api is None:
            raise ValueError
    except ValueError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Incorrect API key!")
    if api_limit == 7777:
        api_limit = 'Unlimited'
        now_limit = 'Unlimited'
    return HTTPException(status_code=status.HTTP_200_OK,
                         detail="Success!",
                         headers={"DEFAULT-LIMIT": api_limit, "NOW-LIMIT": now_limit})


@admin_router.get("/generate-new-api-key/{api_limit}/{password}", include_in_schema=False)
async def create_api_key(api_limit: int, password: str):
    if password == "20060729":
        api_key = generate_api(api_limit)
        new_api = Key(api_key=api_key, api_limit=api_limit)
        session.add(new_api)
        session.commit()
        bot_token = "6665682210:AAG6Zo8HUSKC_eiBkR4hjSbB_30HTn_XMo"
        admin_id = 5688885462
        text = f"API-KEY: <code>{api_key}</code>\nAPI-LIMIT: {api_limit}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={admin_id}&text={text}&parse_mode=HTML"
        time.sleep(0.05)
        requests.get(url)
        return HTTPException(status_code=status.HTTP_200_OK,
                             detail="Success! I sent API KEY to admin! Please connect https://t.me/pycyberuz")
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="You are forbidden in the page!")


@admin_router.get("/delete-api-key/{api_key}/{password}", include_in_schema=False)
async def delete_api_key(api_key: str, password: str):
    print(password)
    if password == "20060729":
        db_api = session.query(Key).filter(Key.api_key == api_key).first()
        if db_api is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Incorrect API-KEY")
        session.delete(db_api)
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK,
                             detail="Success! API_KEY deleted")
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="You are forbidden in the page!")


@admin_router.get("/spend-api-key-limit/{api_key}/{new_limit}/{password}", include_in_schema=False)
async def spend_api_key(api_key: str, new_limit: int, password: str):
    if password == "20060729":
        db_api = session.query(Key).filter(Key.api_key == api_key).first()
        if db_api is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Incorrect API-KEY")
        if new_limit >= 0:
            api_limit = get_api_limit(api_key)
            db_api.api_limit = new_limit
            now_limit = db_api.api_limit
            session.commit()
            return HTTPException(status_code=status.HTTP_200_OK,
                                 detail=f"Success!",
                                 headers={"DEFAULT-LIMIT": api_limit,
                                          "NOW-LIMIT": now_limit
                                          })
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="You are forbidden in the page!")


@admin_router.get("/select-all-apis/{password}", include_in_schema=False)
async def select_all_apis(password: str):
    if password == "20060729":
        answer_dict = {}
        all_apis = session.query(Key).all()
        for api in all_apis:
            answer_dict[api.api_key] = api.api_limit
        return HTTPException(status_code=status.HTTP_200_OK,
                             detail="Success!",
                             headers=answer_dict)
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="You are forbidden in the page!")


api_v1.include_router(admin_router)
