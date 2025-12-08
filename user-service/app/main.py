import json
import logging
import os
import time
from contextlib import asynccontextmanager

import httpx
import redis
from fastapi import FastAPI, HTTPException, Response
from pydantic import EmailStr

from .db import (
    close_db_connection,
    create_user_info,
    delete_user_info,
    get_user_info,
    init_db,
    update_user_info,
)
from .models import UserCreate, UserResponse, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db_connection()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

service = "user-service"

app = FastAPI(lifespan=lifespan)

redis_client = redis.Redis(host=os.getenv(
    "REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", "6379")), decode_responses=True)

CONVENTION_BASE = os.getenv(
    "CONVENTION_BASE", "http://convention-service:8000")
INVENTORY_BASE = os.getenv("INVENTORY_BASE", "http://inventory-service:8000")
TTL_SECONDS = int(os.getenv("TTL_SECONDS", "10000"))


async def response_time(call_fn):
    try:
        start = time.time()
        await call_fn()
        return {"response": "healthy", "response_time_ms": time.time() - start}
    except Exception as e:
        return {"response": "unhealthy", "response_time_ms": time.time() - start}


def format_health_response(service_name, dependencies_health):
    return {
        "service": service_name,
        "status": "healthy",
        "dependencies": dependencies_health
    }


@app.get("/health")
async def health_check():
    try:
        async with httpx.AsyncClient() as client:
            # find a way to healthcheck userdb service
            # convention_resp = await response_time(lambda: client.get(f'{CONVENTION_BASE}/health'))
            inventory_resp = await response_time(lambda: client.get(f'{INVENTORY_BASE}/health'))
            return format_health_response(service, [{"inventory-service": inventory_resp}])
    except Exception as e:
        raise e


@app.get("/user/{user_email}")
async def get_user(user_email: EmailStr) -> Response:
    # check cache (cache-aside) and if fails, get from postgres
    try:
        start_time = time.time()
        cache_resp = redis_client.get(name=user_email)
        if (cache_resp is None):
            logging.info("USER NOT FOUND IN CACHE, CHECKING USERDB")
            # query psql
            psql_resp = get_user_info(user_email)
            if psql_resp is None:
                raise HTTPException(404, "User Not Found")
            logging.info(f'USERDB RESPONSE: {psql_resp}')
            # setex with ttl in cache
            redis_client.setex(user_email, TTL_SECONDS,
                               json.dumps(psql_resp.model_dump()))
            cache_resp = redis_client.get(name=user_email)
        #     cache_dict = psql_resp.model_dump()
        # else:
        #     cache_dict = json.loads(json.dumps(cache_resp))
        logging.info(
            f'RETRIEVED USER: {user_email} WITH PAYLOAD: {cache_resp} IN {time.time() - start_time} MS')
        return Response(cache_resp, status_code=200)
    except Exception as e:
        raise e


@app.post("/create")
async def create_user(new_user: UserCreate):
    try:
        # check if user already exists, throw error
        if get_user_info(new_user.email) is not None:
            raise HTTPException(201, "User with provided email already exists")
        # create a new user using Request body to take in values
        create_user_info(
            new_user.email, new_user.username, new_user.user_type)
        user = get_user_info(new_user.email)
        if not user:
            raise HTTPException(400, "User not created properly")
        logging.info(
            f'CREATED USER IN USERDB: {new_user.email} PAYLOD: {user.model_dump_json(indent=2)}')
        # cache it with TTL and save to postgres
        redis_client.setex(new_user.email, TTL_SECONDS, # type: ignore
                           user.model_dump_json(indent=2))
        logging.info(
            f'CACHED USER: {new_user.email} with fields: {user.model_dump_json(indent=2)}')
        return Response(json.dumps({"status": "created"}), status_code=201)
    except Exception as e:
        raise e


@app.put("/update")
async def update_user(update_user: UserUpdate):
    try:
        # update user in userdb
        user = update_user_info(
            id=update_user.id, username=update_user.username, user_type=update_user.user_type)
        if not user:
            raise HTTPException(404)
        logging.info(f'UPDATED USER {user.email} IN USERDB')
        # setex in redis to update cache and ttl
        redis_client.setex(user.email, TTL_SECONDS,
                           user.model_dump_json())
        logging.info(
            f'CACHED USER: {user.email} with fields: {user.model_dump_json()}')
        return {"status": "updated"}
    except Exception as e:
        raise e

# on hold for now, need to consider cascading across other dbs from other services
@app.delete("/delete")
async def delete_user(user_id: str):
    pass


@app.get("/inv/{user_id}/")
async def get_user_inventory(user_id: str):
    # get user's inventory from inventory-service GET endpoint (should only work if user is a vendor)
    pass


@app.get("/conv/{user_id}/")
async def get_attending_conventions(user_id: str):
    # get list of attending conventions from convention-service GET endpoint
    pass
