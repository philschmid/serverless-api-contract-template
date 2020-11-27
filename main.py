import time
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, HttpUrl, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi.openapi.utils import get_openapi
from uuid import UUID


from fastapi import (
    Body,
    FastAPI,
    Request,
    HTTPException,
    Query,
    Header,
    Depends,
)
from fastapi.middleware.cors import CORSMiddleware

from src import handler


title = "My Serverless API Title"
app = FastAPI(
    title=title,
    redoc_url="/docs",
    docs_url="/x",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=title,
        version="1.0.0",
        description=open("./docs/description.md", "r").read(),
        routes=app.routes,
    )
    openapi_schema["info"]["contact"] = {
        "name": "Serverless API Support",
        "url": "https://www.google.com/contact/",
        "email": "support@google.com",
    }
    openapi_schema["info"]["license"] = {
        "name": "Serverless",
        "url": "https://google.com/api/license/",
    }
    openapi_schema["info"]["termsOfService"] = "https://www.google.com/terms/"

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    openapi_schema["x-tagGroups"] = [
        {"name": "API Calls", "tags": ["items", "custom"]}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


security = HTTPBasic()


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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 3))
    return response


class Item(BaseModel):
    name: str = Field(..., description="The name of the item")
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(
        ..., gt=0, description="The price must be greater than zero"
    )
    tax: Optional[float] = None
    url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class ItemResponse(BaseModel):
    itemId: UUID = Field(..., description="The uuid of the item")
    url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "itemId": "cc2f9990-9771-4072-8eb4-de643c9f4c9d",
                "url": "https://s3.us-west-2.amazonaws.com/mybucket/puppy.jpg",
            }
        }


class ErrorResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Hier steht dein Fehler",
            }
        }


x_my_header = Header(
    None,
    description="send a custom header",
    example="ADFG23123123asdf",
)


@app.post(
    "/item",
    response_model=ItemResponse,
    summary="Create an item",
    responses={404: {"model": ErrorResponse}},
    tags=["items"],
)
async def create_item(
    item: Item,
    x_my_header: Optional[str] = x_my_header,
    credentials: HTTPBasicCredentials = Depends(security),
):
    """
    As a doc string we can provide additional informations in Markdown. https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
    """
    try:
        return item
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=repr(e),
            headers={"X-Error": "There goes my error"},
        )


@app.get("/items/{item_id}", tags=["items"])
async def read_item(
    item_id: str,
    search: Optional[str] = Query(None, max_length=50),
    short: bool = False,
) -> Dict[str, Any]:
    try:
        # event = await _event(request)
        return {"item": item_id}
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=repr(e),
            headers={"X-Error": "There goes my error"},
        )


@app.put(
    "/items/{item_id}",
    tags=["items"],
)
async def update_item(item_id: int, item: Item):
    if item_id not in item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, **item.dict()}


@app.put(
    "/it",
    tags=["custom"],
)
async def test_custom_field_body(
    item_id: str = Body(
        ..., title="The ID of the item to get", example="uasdga1-afg3i-fdg"
    ),
    importance: int = Body(
        ..., title="The Importance for the request", ge=1, example=3
    ),
    description: str = Body(
        ...,
        title="The Description for the item",
        min_length=3,
        max_length=50,
        regex="^A-Za-z0-9$",
        example="This is a nice item",
    ),
    required: bool = Body(..., example=True),
):
    results = {
        "item_id": item_id,
        "importance": importance,
    }
    return results


app.openapi = custom_openapi
