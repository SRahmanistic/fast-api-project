from fastapi import APIRouter, Depends, status,HTTPException
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog

get_db = database.get_db
router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.get("/getall", response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.get("/get/{id}", status_code=200, response_model=schemas.ShowBlog)
def one_blog(id: int,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get(id,db)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_blog(new_blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(new_blog, db)

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id,db)

@router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request,db)
