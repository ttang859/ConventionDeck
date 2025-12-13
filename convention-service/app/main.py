import json
import logging
import os
import time
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException

from .db import (
    close_db_connection,
    create_convention,
    delete_convention,
    get_convention_by,
    init_db,
    update_convention,
)
from .models import (
    ConventionCreate,
    ConventionDelete,
    ConventionRetrieve,
    ConventionUpdate,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db_connection()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = FastAPI(lifespan=lifespan)

service = "convention-service"

# redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(
#     os.getenv("REDIS_PORT", 6379)), decode_responses=True)

# BOOTH_BASE = os.getenv("BOOTH_BASE", "http://booth-service:8000")
# REGISTRATION_BASE = os.getenv(
#     "REGISTRATION_BASE", "http://registration-service:8000")


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
        # async with httpx.AsyncClient() as client:
        #     booth_resp = await response_time(lambda: client.get(f'{BOOTH_BASE}/health'))
        #     registration_resp = await response_time(lambda: client.get(f'{REGISTRATION_BASE}/health'))
        return format_health_response(service, [{}])
    except Exception as e:
        raise HTTPException(503, e)


@app.post("/create")
async def create_conv(convention: ConventionCreate):
    try:
        logging.info(f'CREATING CONVENTION {convention}')
        id = create_convention(conv_name=convention.convention_name,
                               host_id=convention.host_id, loc=convention.loc, start_datetime=convention.start)
        logging.info(f'SUCCESSFULLY CREATED CONVENTION WITH ID {id}')
        return {"conv_id": id}
    except Exception as e:
        raise e


@app.post("/get")
async def get_conv(options: ConventionRetrieve):
    try:
        if not options.conv_id and not options.host_id:
            logging.info("RETRIEVING ALL CONVENTIONS")
        elif options.host_id:
            logging.info(
                f'RETRIEVING CONVENTION(S) BY HOST_ID {options.host_id}')
        else:
            logging.info(f'RETREIVING CONVENTION BY CONV_ID {options.conv_id}')
        conventions = get_convention_by(
            conv_id=options.conv_id, host_id=options.host_id)
        logging.info(f'SUCCESSFULLY RETRIEVED CONVENTION(S)')
        return {"payload": conventions}
    except Exception as e:
        raise e


@app.put("/update")
async def update_conv(options: ConventionUpdate):
    try:
        logging.info(f'UPDATING DETAILS FOR CONVENTION {options.id}')
        update_convention(conv_id=options.id, start_datetime=options.start,
                          loc=options.loc, vendor_count=options.vendor_count)
        logging.info(f'UPDATED CONVENTION {options.id}')
        return {"status": "updated"}
    except Exception as e:
        raise e


@app.delete("/delete")
async def delete_conv(convention: ConventionDelete):
    try:
        logging.info(f'DELETING {convention.id}')
        delete_convention(conv_id=convention.id)
        logging.info("SUCCESSFUL DELETE")
        return {"status": "deleted"}
    except Exception as e:
        raise e
