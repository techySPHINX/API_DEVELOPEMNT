from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Pydantic Model


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # defining integer


# request Get method url : "/"

my_posts = [{"title": "title of post 1", "content": "Content of post 1", "id": 1}, {
    "title": "title of post 2", "content": "Content of post 2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Welcome to JK api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    # print(payLoad)  # this is basically to take out the data
    # return {"message": "successfully created posts"}
    # return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
    # print(post)
    # print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)  # to create unique id
    my_posts.append(post_dict)
    return {"data": "post_dict"}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))
    return {"post_detail": f"Here is post {id}"}
