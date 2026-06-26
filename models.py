from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,nullable=False)
    age =  Column(Integer,nullable=False)
    gender = Column(String(15),nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    password = Column(String(200),nullable=False)
    phone_number = Column(String(13), nullable=False, unique=True)
    city = Column(String(30),nullable=False)
    role = Column(String,default="user")
    profile_image = Column(String,nullable=True)
    blogs = relationship("Blog",back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),unique=True,nullable=False)
    blogs = relationship("Blog",back_populates="category")

class Blog(Base):
    __tablename__="blogs"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(200),nullable=False,unique=True,)
    content = Column(String(1000),nullable=False)
    image = Column(String,nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer,ForeignKey("categories.id"))
    #category_name = Column(String)
    user = relationship("User",back_populates="blogs")
    category = relationship("Category",back_populates="blogs")
    