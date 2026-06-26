from pydantic import BaseModel, Field
from typing import Literal
import re

class UserCreate(BaseModel):
    username:str = Field(pattern=r"^[A-Za-z ]{3,30}$")
    age:int = Field(ge=1, le=999)
    gender:Literal["Male", "Female", "Not Disclose"]
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@gmail\.com$")
    password: str
    phone_number: str =Field(pattern=r"^\+91[1-9][0-9]{9}$")
    city:str =Field(pattern=r"^[A-Za-z ]{2,30}$")
    '''
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 10:
            raise ValueError("Password minimum 10 characters required")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain capital letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain small letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain number")
        if not re.search(r"[@#$%^&+=!]", value):
            raise ValueError("Password must contain special character")
        return value
'''
#login
class UserLogin(BaseModel):
    email:str
    password:str

#blog create
class BlogCreate(BaseModel):
    title:str
    content:str
    category_id: int
    #user_id:int
    
    

#blog response
class BlogResponse(BaseModel):
    id:int
    title:str
    content:str
    user_id:int |None
    image:str | None = None
    category:CategoryResponse | None = None
    class Config:
        from_attributes=True

#user response
class UserResponse(BaseModel):
    id:int
    username:str
    age:int
    gender:str
    email:str
    phone_number:str
    city:str
    class Config:
        from_attributes=True 
      
#create category    
class CategoryCreate(BaseModel):
    name: str

#category response
class CategoryResponse(BaseModel):
    id:int
    name:str
    '''user_id:int | None
    title:str
    content:str
    category:CategoryResponse
    '''
    class Config:
        from_attributes=True      