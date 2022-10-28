from fastapi import FastAPI, status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from fastapi.params import Body
from typing import Optional, Any
from pydantic import BaseModel
from random import randrange
import datetime
import psycopg2
import uvicorn

app = FastAPI()
my_post = []


class Post(BaseModel):
    # *Basic parameters in the dict
    title: str
    content: str
    published: bool = True
    rating: float = 0.0


@ app.get("/post")
def root():
    # *Func to JUST read the available posts.
    return my_post


@ app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(newPost: Post, response: Response):
    # *Func to created new posts.
    date = datetime.datetime.now()
    if not newPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data = newPost.dict()
    data["published_date"] = date.strftime("%y/%m/%d")
    my_post.append(data)
    data["id"] = len(my_post)
    return my_post


def find_post(id):
    # *Func to run trough all the posts stored.
    for post in my_post:
        if post["id"] == id:
            return post


def find_index_id(id):
    # *Func to find the post id in the array
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


@ app.get("/post/{id}")
def get_id(id: int):
    if data := find_post(id):
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the id:{id} was not found")


@ app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):  # sourcery skip: raise-from-previous-error
    try:
        index = find_index_id(id)
        my_post.pop(index)  # type: ignore
    except TypeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/post/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):  # sourcery skip: raise-from-previous-error
    try:
        index = find_index_id(id)
        post_dict = post.dict()
        post_dict["id"] = id
        my_post[index] = post_dict  # type: ignore
    except TypeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} does not exist")

    return {"data": post_dict}


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
