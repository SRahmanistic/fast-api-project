from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


@app.get("/blog")
async def blogs(limit: int = 10, published: bool = True):

   if published:
      return {"data": f"{limit} published blogs fetched"}
   else:
      return {"data": f"{limit} non published blogs fetched"}
