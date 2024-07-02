from fastapi import FastAPI

app = FastAPI()

#request Get method url : "/"

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data":"This is your posts"}