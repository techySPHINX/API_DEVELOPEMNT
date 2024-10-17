from enum import Enum

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()


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


# make sure to put this before dynamic lower one so that it would play first
@app.get("/users/me")
async def get_current_user():
    return {"Message": "this is the current user"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}


class RoleEnum(str, Enum):
    manager = "manager"
    developer = "developer"
    designer = "designer"


@app.get("/roles/{role_name}")
async def get_role(role_name: RoleEnum):
    if role_name == RoleEnum.manager:
        return {"role_name": role_name, "message": "you manage things"}

    if role_name.value == "developer":
        return {
            "role_name": role_name,
            "message": "you develop things",
        }
    if role_name.value == "designer":
        return {
            "role_name": role_name,
            "message": "you design things",
        }
    return {"role_name": role_name, "message": "unknown role"}

# you could try with salary as role_name key's values and play with that; ex : salaries as values
# class RoleEnum(str, Enum):
#     manager = "50000"
#     developer = "40000"
#     designer = "35000"

fake_items = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items[skip: skip + limit]


@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, details: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if details:
        item.update(
            {
                "description": "This is a detailed description of the item.",
                "price": 100,
                "availability": "In stock"
            }
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {
        "item_id": item_id,
        "owner_id": user_id,
        "name": "Sample Item",
        "category": "Electronics",
        "price": 299.99,
        "availability": "In stock"
    }
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is a detailed description of the item, including its features, specifications, and usage instructions.",
                "warranty": "2 years",
                "manufacturer": "Example Corp"
            }
        )
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items")
async def read_items(
    q: str
    | None = Query(
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
    hidden_query: str | None = Query(None, include_in_schema=False)
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
