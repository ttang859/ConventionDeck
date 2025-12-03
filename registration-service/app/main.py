import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis.asyncio as redis
import os

service = "registration-service"

app = FastAPI()

redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(
    os.getenv("REDIS_PORT", 6379)), decode_responses=True)

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
        redis_resp = await response_time(lambda: redis_client.ping())
        return format_health_response(service, [{"redis": redis_resp}])
    except Exception as e:
        raise HTTPException(503)
