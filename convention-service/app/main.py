import json
import os
import time

import httpx
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

service = "convention-service"

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(
    os.getenv("REDIS_PORT", 6379)), decode_responses=True)

BOOTH_BASE = os.getenv("BOOTH_BASE", "http://booth-service:8000")
REGISTRATION_BASE = os.getenv(
    "REGISTRATION_BASE", "http://registration-service:8000")

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
            booth_resp = await response_time(lambda: client.get(f'{BOOTH_BASE}/health'))
            registration_resp = await response_time(lambda: client.get(f'{REGISTRATION_BASE}/health'))
            redis_resp = await response_time(lambda: redis_client.ping())
        return format_health_response(service, [{"booth-service": booth_resp}, {"registration-service": registration_resp},{"redis": redis_resp}])
    except Exception as e:
        raise HTTPException(503, e)
