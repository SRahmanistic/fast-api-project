from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get-blogs", response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/get-blog/{id}", status_code=200, response_model=schemas.ShowBlog)
def one_blog(id: int,response: Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} not available'}
    return blog

@app.post("/create-blog", status_code=status.HTTP_201_CREATED)
async def create_blog(new_blog: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=new_blog.title, body= new_blog.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog


@app.delete("/delete-blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put("/update-blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
    
    db.query(models.Blog).filter(models.Blog.id == id).update(request.dict())
    db.commit()
    return 'updated'

