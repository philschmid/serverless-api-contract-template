import time
import os
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src import handler


app = FastAPI()


origins = [
    # os['environ']['ORIGIN'],
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _event(request: Request) -> Dict[str, Any]:
    event: Dict[str, Any] = {}
    event["headers"] = dict(request.headers.items())
    event["method"] = request.method
    try:
        event["body"] = await request.json()
    except KeyError:
        pass
        # raise Exception('No Body in Request')
    finally:
        return event


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 3))
    return response


@app.get("/")
async def call_handler(request: Request):
    try:
        event = await _event(request)
        context = os.getenv("HOSTNAME", "localhost")
        function_return = handler.handler(event, context)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=repr(e),
            headers={"X-Error": "There goes my error"},
        )

    return function_return
