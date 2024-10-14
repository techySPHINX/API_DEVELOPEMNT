from enum import Enum

from fastapi import FastAPI

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
