from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from security import hash_password
from security import verify_password
from auth import create_token
from fastapi import UploadFile, File,Form
import shutil
import os
router = APIRouter()
from auth_dependency import get_current_user


# Signup (No token required)
@router.post("/signup")
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    '''
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
        '''
    
    hashed_password = hash_password(user.password)


    new_user = models.User(
        username=user.username,
        age=user.age,
        gender=user.gender,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number,
        city=user.city,
        role="user"
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message":"Signup successful",
        "user_id":new_user.id
    }



# Login (No token required)
@router.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )
    '''
    if db_user.password != user.password:
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )
        '''
    token = create_token(
        {
            "user_id": db_user.id,
            "email": db_user.email,
            "role": db_user.role
        }
    )
    return {
        "access_token":token,
        "token_type":"bearer"
    }

@router.post("/upload-profile/{user_id}")
def upload_profile_image(
    user_id:int,
    file:UploadFile=File(...),
    db:Session=Depends(get_db)
):

    user=db.query(models.User).filter(
        models.User.id==user_id
    ).first()


    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    # allowed image formats
    allowed_extensions = [
        "jpg",
        "jpeg",
        "png"
    ]


    # get file extension
    file_extension = file.filename.split(".")[-1].lower()


    # check condition
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only jpg, jpeg and png images are allowed"
        )
    file_location=f"uploads/{file.filename}"
    
    # duplicate image check
    if os.path.exists(file_location):

        raise HTTPException(
            status_code=400,
            detail="Image already exists"
        )

    #save the file
    with open(file_location,"wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )
    #save only file name in database
    user.profile_image=file.filename
    db.commit()
    db.refresh(user)
    return {
        "message":"Image uploaded successfully",
        "file_name":user.profile_image
    }

# User can see only own data
@router.get("/me")
def get_my_profile(
    request: Request,
    db: Session = Depends(get_db)
):
   
    if not hasattr(request.state, "user") or request.state.user is None:
        raise HTTPException(
            status_code=401,
            detail="Please provide valid token"
        )
    user_id = request.state.user["user_id"]

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    return {
        "id": user.id,
        "username": user.username,
        "age": user.age,
        "gender": user.gender,
        "email": user.email,
        "phone_number": user.phone_number,
        "role": user.role,
        "city": user.city,
        "profile_image": f"{request.base_url}uploads/{user.profile_image}"
    }


# Only creator can see all users
@router.get("/users")
def all_users(
    request: Request,
    db: Session = Depends(get_db)
):
    
    if request.state.user is None:
        raise HTTPException(
            status_code=401,
            detail="Please provide token"
        )
    role = request.state.user["role"]

    if role != "creator":
        raise HTTPException(
            status_code=403,
            detail="Only creator can access"
        )
    users = db.query(models.User).all()
    return users
'''
@router.get(
    "/blogs",
    response_model=list[schemas.BlogResponse]
)
def get_blogs(
    db:Session=Depends(get_db)
):
    blogs = db.query(
        models.Blog
    ).all()
    return blogs
'''

@router.post("/blogs")
def create_blog(

    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    request: Request = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]
    # image validation
    allowed = [
        "jpg",
        "jpeg",
        "png"
    ]
    extension = image.filename.split(".")[-1].lower()
    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Only jpg jpeg png allowed"
        )
    file_location = f"uploads/{image.filename}"
    if os.path.exists(file_location):
        raise HTTPException(
            status_code=400,
            detail="Image already exists"
        )
    with open(file_location,"wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )



    new_blog = models.Blog(

        title=title,

        content=content,

        category_id=category_id,

        user_id=user_id,

        image=image.filename

    )


    db.add(new_blog)

    db.commit()

    db.refresh(new_blog)



    return {

        "message":"Blog created successfully",

        "id":new_blog.id,

        "title":new_blog.title,

        "content":new_blog.content,

        "category_id":new_blog.category_id,

        "user_id":new_blog.user_id,

        "image":f"{request.base_url}uploads/{new_blog.image}"
    }

'''
    user_id=request.state.user["user_id"]

    # image check
    allowed=[
        "jpg",
        "jpeg",
        "png"
    ]
    
    file_location=f"uploads/{image.filename}"

    with open(file_location,"wb") as buffer:

        shutil.copyfileobj(
            image.file,
            buffer
        )
    new_blog=models.Blog(
        title=title,
        content=content,
        category_id=category_id,
        user_id=user_id,
        image=image.filename
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
'''
@router.get("/blogs")
def get_blogs(
    request: Request,
    db:Session=Depends(get_db)
):

    blogs=db.query(models.Blog).all()


    return [

        {
            "id":blog.id,

            "title":blog.title,

            "content":blog.content,

            "category_id":blog.category_id,

            "user_id":blog.user_id,

            "image":
            f"{request.base_url}uploads/{blog.image}"

        }

        for blog in blogs
    ]
@router.get("/categories")
def get_categories(
    db:Session=Depends(get_db)
):
    return db.query(
        models.Category
    ).all()