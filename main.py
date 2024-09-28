from datetime import datetime, time, timedelta
from enum import Enum
from uuid import UUID

from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

app = FastAPI()

'''
@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post("/")
async def post():
    return {"message": "hello from the post route"}


@app.put("/")
async def put():
    return {"message": "hello from the put route"}


@app.get("/users")
async def list_users():
    return {"message": "list users route"}


@app.get("/users/me")
async def get_current_user():
    return {"Message": "this is the current user"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}

    if food_name.value == "fruits":
        return {
            "food_name": food_name,
            "message": "you are still healthy, but like sweet things",
        }
    return {"food_name": food_name, "message": "i like chocolate milk"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def get_item(
    item_id: str, sample_query_param: str, q: Optional[str], short: bool = False
):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur."
            }
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int, item_id: str, q: Optional[str], short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur."
            }
        )
        return item


class Item(BaseModel):
    name: str
    description: Optional[str]
    price: float
    tax: Optional[float]


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: Optional[str]):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items")
async def read_items(
    q: Optional[str] = Query(
        None,
        min_length=3,
        max_length=10,
        title="Sample query string",
        description="This is a sample query string.",
        alias="item-query",
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_hidden")
async def hidden_query_route(
    hidden_query: Optional[str] = Query(None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}

@app.get("/items_validation/{item_id}")
async def read_items_validation(
    *,
    item_id: int = Path(..., title="The ID of the item to get", gt=10, le=100),
    q: str = "hello",
    size: float = Query(..., gt=0, lt=7.75)
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results




# Part 7 -> Body - Multiple Parameters
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
    q: Optional[str] = None,
    item: Item = Body(..., embed=True),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

    

## Part 8 -> Body - Fields
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero.")
    tax: Optional[float]  = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results



## Part 9 -> Body - Nested Models


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []
    image: Optional[List[Image]]  = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers")
async def create_offer(offer: Offer = Body(..., embed=True)):
    return offer


@app.post("/images/multiple")
async def create_multiple_images(images: List[Image]):
    return images



## Part 10 - Declare Request Example Data
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 16.25,
    #             "tax": 1.67,
    #         }
    #     }


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A __normal__ item works _correctly_",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 16.25,
                    "tax": 1.67,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {"name": "Bar", "price": "16.25"},
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "description": "Hello My People",
                "value": {"name": "Baz", "price": "sixteen point two five"},
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results



## Part 11 - Extra Data Types
@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_date: Optional[datetime] = Body(None),
    end_date: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_date + process_after
    duration = end_date - start_process
    return {
        "item_id": item_id,
        "start_date": start_date,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
'''

## Part 12 - Cookie and Header Parameters
@app.get("/items")
async def read_items(
    cookie_id: Optional[str] = Cookie(None),
    accept_encoding: Optional[str] = Header(None),
    sec_ch_ua: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    x_token: Optional[List[str]] = Header(None),
):
    return {
        "cookie_id": cookie_id,
        "Accept-Encoding": accept_encoding,
        "sec-ch-ua": sec_ch_ua,
        "User-Agent": user_agent,
        "X-Token values": x_token,
    }


