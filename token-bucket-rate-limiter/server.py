import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BUCKET_CAPACITY = 10 # we usually use redis instead of global variable in production
REFILL_RATE     = 1


tokens: float        = BUCKET_CAPACITY
last_refill_time: float = time.time()

app = FastAPI(title="Token Bucket Rate Limiter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _refill() -> None:
    global tokens, last_refill_time
    now = time.time()
    elapsed = now - last_refill_time
    tokens = min(BUCKET_CAPACITY, tokens + elapsed * REFILL_RATE)
    last_refill_time = now


class BucketStatus(BaseModel):
    tokens: float
    capacity: int
    refill_rate: int

class RequestResult(BaseModel):
    allowed: bool
    tokens: float
    capacity: int
    refill_rate: int
    message: str


@app.get("/status", response_model=BucketStatus)
def get_status():
    _refill()
    return BucketStatus(
        tokens=round(tokens, 2),
        capacity=BUCKET_CAPACITY,
        refill_rate=REFILL_RATE,
    )


@app.get("/request", response_model=RequestResult)
def make_request():
    global tokens
    _refill()

    if tokens >= 1:
        tokens -= 1
        return RequestResult(
            allowed=True,
            tokens=round(tokens, 2),
            capacity=BUCKET_CAPACITY,
            refill_rate=REFILL_RATE,
            message="✅ Request allowed",
        )
    else:
        return RequestResult(
            allowed=False,
            tokens=round(tokens, 2),
            capacity=BUCKET_CAPACITY,
            refill_rate=REFILL_RATE,
            message="🚫 Rate limited — not enough tokens",
        )


@app.post("/reset")
def reset_bucket():
    global tokens, last_refill_time
    tokens = BUCKET_CAPACITY
    last_refill_time = time.time()
    return {"message": "Bucket reset", "tokens": BUCKET_CAPACITY}
