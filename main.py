from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import  BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None # defining integer
    

# request Get method url : "/"


@app.get("/")
async def root():
    return {"message": "Welcome to my api"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_posts(post: Post):
    # print(payLoad)  # this is basically to take out the data
    # return {"message": "successfully created posts"}
    # return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
    print(post)
    print(post.dict())
    return {"data": "post"}
