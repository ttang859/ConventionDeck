import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .db import (
    assign_booth,
    close_db_connection,
    create_booth,
    init_db,
    remove_booth,
    retrieve_booth,
    unassign_booth,
)
from .models import AllBooths, BoothAssignmentResp, GetBoothOptions, ValidAssignment


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

service = "booth-service"

# redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(
#     os.getenv("REDIS_PORT", 6379)), decode_responses=True)


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


@app.post("/create_all")
async def create_convention_booths(options: AllBooths):
    try:
        logging.info(
            f'CREATING {options.total_booths} BOOTHS FOR CONVENTION ID {options.conv_id}')
        for i in range(1, options.total_booths+1):
            create_booth(conv_id=options.conv_id, booth_number=i)
            logging.debug(f'created booth no. {i}')
        logging.info(f'CREATED {options.total_booths} NEW BOOTHS')
        return {"status": "created", "num_booths": options.total_booths}
    except Exception as e:
        raise e


@app.post("/get")
async def get_booths_by(options: GetBoothOptions):
    try:
        if options.conv_id and options.vendor_id:
            logging.info(
                f'RETRIEVING BOOTH BY CONV_ID {options.conv_id} AND VENDOR_ID {options.vendor_id}')
        elif options.conv_id:
            logging.info(f'RETRIEVING BOOTH BY CONV_ID {options.conv_id}')
        elif options.vendor_id:
            logging.info(f'RETRIEVING BOOTH BY VENDOR_ID {options.vendor_id}')
        else:
            logging.info("NO OPTIONS SPECIFIED, UNABLE TO RETRIEVE")
            return None
        return retrieve_booth(conv_id=options.conv_id, vendor_id=options.vendor_id)
    except Exception as e:
        raise e


@app.put("/assign_vendor")
async def assign_vendor(options: ValidAssignment):
    try:
        logging.info(
            f'ASSIGNING VENDOR ID {options.vendor_id} TO BOOTH NO. {options.booth_number} IN CONVENTION {options.conv_id}')
        rowcount = assign_booth(
            conv_id=options.conv_id, vendor_id=options.vendor_id, booth_number=int(options.booth_number))
        if rowcount > 0:
            logging.info(
                f'SUCCESSFULLY ASSIGNED VENDOR ID {options.vendor_id} TO BOOTH NO. {options.booth_number} IN CONVENTION {options.conv_id}')
        else:
            logging.info("UNABLE TO ASSIGN BOOTH")
        return rowcount
    except Exception as e:
        raise e


@app.put("/unassign_vendor")
async def unassign_vendor(options: ValidAssignment):
    try:
        logging.info(
            f'UNASSIGNING VENDOR ID {options.vendor_id} TO BOOTH NO. {options.booth_number} IN CONVENTION {options.conv_id}')
        rowcount = unassign_booth(
            conv_id=options.conv_id, booth_number=options.booth_number)
        if rowcount > 0:
            logging.info(
                f'SUCCESSFULLY UNASSIGNED VENDOR ID {options.vendor_id} TO BOOTH NO. {options.booth_number} IN CONVENTION {options.conv_id}')
        else:
            logging.info("UNABLE TO ASSIGN BOOTH")
        return rowcount
    except Exception as e:
        raise e


@app.delete("/delete_all")
async def delete_convention_booths(options: AllBooths):
    try:
        logging.info(f'DELETING ALL BOOTHS FOR CONVENTION {options.conv_id}')
        for i in range(1, options.total_booths+1):
            remove_booth(conv_id=options.conv_id, booth_number=i)
            logging.debug(f'deleted booth no. {i}')
        logging.info(
            f'SUCCESSFULLY DELETED ALL BOOTHS FOR CONVENTION {options.conv_id}')
        return {"status": "deleted", "num_booths": options.total_booths}
    except Exception as e:
        raise e
