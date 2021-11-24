from sqlalchemy.orm import Session
from .. import models

def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs

def get(id, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not available')
    return blog

def create(new_blog,db):
    newBlog = models.Blog(title=new_blog.title, body= new_blog.body, user_id=1)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog 