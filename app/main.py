from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Welcome to JK api"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
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


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:

        # type: ignore # the best approach
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = 404 # approach of hard-coding
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id: {id} was not found"}
    return {"post_detail": f"Here is post {id}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required
    # my_posts.pop(index)
    index = find_post_index(id)

    if index == None:
        # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail = f"post with id: {id} was not found")

    my_posts.pop(index)
    # return {'message': "post was successfully deleted"}
    # if we dont need data sending back only status
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)

    if index == None:
        # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail = f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}
    # return {'message': "post updated succesfully"}
