from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get-blogs", response_model=List[schemas.ShowBlog], tags=['Blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/get-blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=['Blogs'])
def one_blog(id: int,response: Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
    return blog

@app.post("/create-blog", status_code=status.HTTP_201_CREATED, tags=['Blogs'])
async def create_blog(new_blog: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=new_blog.title, body= new_blog.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog


@app.delete("/delete-blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put("/update-blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(id: int, request: schemas.Blog,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
    
    db.query(models.Blog).filter(models.Blog.id == id).update(request.dict())
    db.commit()
    return 'updated'


@app.post("/create-user", response_model=schemas.ShowUser, tags=['Users'])
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/get-user/{id}", response_model=schemas.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not available')
    return user