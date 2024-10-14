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


@app.get("/users/me")  # make sure to put this before dynamic lower one so that it would play first
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
    


