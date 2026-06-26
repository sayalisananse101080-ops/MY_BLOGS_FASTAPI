from sqlalchemy.orm import Session
import models
from auth import hash_password


#signup-create user
def create_user(db:Session,user):

    new_user=models.User(

        username=user.username,
        age=user.age,
        gender=user.gender,
        email=user.email,
        password=hash_password(user.password),
        phone_number=user.phone_number,
        city=user.city,

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user


#get user (login + ME API)
def get_user(db,email):


    return db.query(
        models.User
    ).filter(
        models.User.email==email
    ).first()





'''def get_user(db,email):

    return db.query(models.User).filter(
        models.User.email==email
    ).first()

# Login - get user by email
def get_user(db, email):

    user = db.query(
        models.User
    ).filter(
        models.User.email == email
    ).first()


    return user

'''
#create a blog (add)
def create_blog(db,blog,user_id):

    new_blog=models.Blog(

        title=blog.title,

        content=blog.content,

        owner_id=user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#get all blogs
def get_blogs(db):

    return db.query(
        models.Blog
    ).all()

#delete blogs
def delete_blog(db,id):

    blog=db.query(
        models.Blog
    ).filter(
        models.Blog.id==id
    ).first()

    if blog:

        db.delete(blog)

        db.commit()

    return blog