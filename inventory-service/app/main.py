import os
import time

from fastapi import FastAPI, HTTPException

service = "inventory-service"

app = FastAPI()

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

@app.get("/getitem/{owner_id}")
async def get_all_inv(owner_id: str):
    if owner_id:  # if owner_id specifed, retrieve all items for that owner_id
        pass
    else: #drop the entire list of available inventory (good idea? prob not)
        pass
