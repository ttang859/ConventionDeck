import json
import logging
import os
import time
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from .db import close_db_connection, get_attending_conventions, get_convention_attendees, register_user, unregister_user
from .models import RegisteredPair


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init_db()
    yield
    close_db_connection()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = FastAPI(lifespan=lifespan)

service = "registration-service"


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
        # redis_resp = await response_time(lambda: redis_client.ping())
        return format_health_response(service, [{}])
    except Exception as e:
        raise HTTPException(503)


@app.post("/register_user")
async def register(options: RegisteredPair):
    try:
        logging.info(
            f'ATTENDEE {options.attendee_id} IS REGISTERING FOR CONVENTION {options.conv_id}')
        register_user(conv_id=options.conv_id, attendee_id=options.attendee_id)
        logging.info(f'REGISTRATION SUCCESSFUL')
        return {"status": "registered"}
    except Exception as e:
        raise e

@app.delete("/unregister_user")
async def unregister(options: RegisteredPair):
    try:
        logging.info(
            f'ATTENDEE {options.attendee_id} IS UNREGISTERING FOR CONVENTION {options.conv_id}')
        unregister_user(conv_id=options.conv_id,
                        attendee_id=options.attendee_id)
        logging.info(f'UNREGISTRATION SUCCESSFUL')
        return {"status": "unregistered"}
    except Exception as e:
        raise e

@app.post("/get_attendees/{conv_id}")
async def attendee_list(conv_id):
    try:
        # validate conv_id
        logging.info(f'RETRIEVING ATTENDEES FOR CONVENTION {conv_id}')
        list = get_convention_attendees(conv_id=conv_id)
        logging.info(f'RETURNED LIST OF ATTENDEES FOR CONVENTION {conv_id}')
        return Response(json.dumps({"payload": list}))
    except Exception as e:
        raise e

@app.post("/get_conventions/{user_id}")
async def convention_list(user_id):
    try:
        # validate user_id
        logging.info(f'RETRIEVING ATTENDEES FOR CONVENTION {user_id}')
        list = get_attending_conventions(attendee_id=user_id)
        logging.info(f'RETURNED LIST OF ATTENDEES FOR CONVENTION {user_id}')
        return Response(json.dumps({"payload": list}))
    except Exception as e:
        raise e
