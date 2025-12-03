import os
import time
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    username: str
    user_type: Literal["vendor", "attendee"]

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    user_type: Literal["vendor", "attendee"]

service = "user-service"

app = FastAPI()

CONVENTION_BASE = os.getenv(
    "CONVENTION_BASE", "http://convention-service:8000")
INVENTORY_BASE = os.getenv("INVENTORY_BASE", "http://inventory-service:8000")


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
            convention_resp = await response_time(lambda: client.get(f'{CONVENTION_BASE}/health'))
            inventory_resp = await response_time(lambda: client.get(f'{INVENTORY_BASE}/health'))
            return format_health_response(service, [{"convention-service": convention_resp}, {"inventory-service": inventory_resp}])
    except Exception as e:
        raise HTTPException(503)


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    # check cache (cache-aside) and if fails, get from postgres
    pass

@app.put("/user/create")
async def create_user(req: Request):
    # create a new user using Request body to take in values
    # cache it with TTL and save to postgres
    pass

@app.get("/user/{user_id}/inventory")
async def get_user_inventory(user_id: str):
    # get user's inventory from inventory-service GET endpoint (should only work if user is a vendor)
    pass

@app.get("/user/{user_id}/conventions")
async def get_attending_conventions(user_id: str):
    # get list of attending conventions from convention-service GET endpoint
    pass
