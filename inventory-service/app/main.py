import json
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Response

from .db import close_db_connection, create_card_entry, get_card_entries, init_db, update_card_entry, delete_card_entry
from .models import InventoryCreate, InventoryDelete, InventoryRetrieve, InventoryUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db_connection()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

service = "inventory-service"

app = FastAPI(lifespan=lifespan)


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
        return format_health_response(service, [{}])
    except Exception as e:
        raise HTTPException(503)


# has an owner_id filter to pull up a list of all cards associated to an owner (owner's card inventory)
@app.post("/get")
async def get_all_inv(req: Optional[InventoryRetrieve] = None):
    try:
        if req:
            owner_id = req.owner_id
            logging.info(f'LOOKING FOR {owner_id}')
        else:
            owner_id = None
            logging.info("RETRIEVING ALL CARDS")
        db_resp = get_card_entries(owner_id)
        return Response(json.dumps({"payload": db_resp}))
    except Exception as e:
        raise e


@app.post("/create")
async def create_inv_entry(entry: InventoryCreate):
    try:
        logging.info(f'CREATING NEW INV ENTRY FOR USER {entry.owner_id}')
        create_card_entry(card_name=entry.card_name,
                          owner_id=entry.owner_id, price=entry.price)
        logging.info('SUCCESSFUL CREATION OF INV ENTRY')
        return {"status": "created"}
    except Exception as e:
        raise e

# given more time, would need to authenticate to ensure proper user is the one that is allowed to update specific card
@app.put("/update")
async def update_inv_entry(entry: InventoryUpdate):
    try:
        update_card_entry(card_id=entry.id, price=entry.price)
    except Exception as e:
        raise e


@app.delete("/delete")
async def delete_inv_entry(entry: InventoryDelete):
    try:
        delete_card_entry(card_id=entry.id)
    except Exception as e:
        raise e
