from fastapi import FastAPI,Depends, HTTPException, APIRouter,Request
from sqlalchemy.orm import Session
from database import engine,SessionLocal ,get_db
from routers import users
#from middleware import auth_middleware   # <-- add this
from auth import create_token
from auth import verify_token
import models
import schemas
import crud
from security import hash_password
from security import verify_password
from fastapi.security import HTTPBearer
from fastapi import Security
#from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
#app.middleware("http")(auth_middleware)
app.include_router(users.router)
router = APIRouter()
security = HTTPBearer()
def get_current_user(
    credentials = Security(security)
):

    token = credentials.credentials

    data = verify_token(token)
    if "user_id" not in data:
        raise HTTPException(
            status_code=401,
            detail="Invalid token data"
        )

    return data



# database connection
'''
# <-- add middleware here
app.middleware("http")(auth_middleware)
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#home api
@app.get("/")
def home():
    return {
        "message":" BLOG API running"
    }
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

#signup API - create user
@app.post("/signup")
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = crud.get_user(
        db,
        user.email
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    new_user = models.User(
        username=user.username,
        age=user.age,
        gender=user.gender,
        email=user.email,
        #password=user.password,
        password=hash_password(user.password),
        phone_number=user.phone_number,
        city=user.city
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #new_user = crud.create_user(db, user)
    return {
        "message": "Signup successful",
        "username": new_user.username,
        "email": new_user.email,
        "phone_number": new_user.phone_number,
        "city":new_user.city,
        "age":new_user.age,
        "gender":new_user.gender
    }
#login API JWT TOKEN
'''
@app.post("/login")
def login(
    user:schemas.UserLogin,
    db:Session=Depends(get_db)
):
    db_user = crud.get_user(
        db,
        user.email
    )
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )
    token=create_token(
        {
            "email":db_user.email
        }
    )
    return {
        "message":"Login successful",
        "access_token":token,
        "token_type":"bearer"
    }
'''

@app.post("/login")
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

    # password checking here
    if not verify_password(
        user.password,          # password entered by user
        db_user.password        # hashed password from MySQL
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )
    token = create_token(
        {
            "user_id": db_user.id,
            "email": db_user.email
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
'''api_key = APIKeyHeader(
    name="Authorization",
    auto_error=False
)'''
#Make uploads folder visible
app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")

#add ME API
@app.get("/me", response_model=schemas.UserResponse)
def me(
    credentials = Security(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials
    print("TOKEN RECEIVED:", token)


    data = verify_token(token)
    print("TOKEN DATA:", data)


    user_id = data["user_id"]


    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
'''
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    print("REQUEST PATH:", request.url.path)
    public_routes = [
        "/signup",
        "/login",
        "/docs",
        "/openapi.json"
    ]


    if request.url.path in public_routes:
        return await call_next(request)


    auth_header = request.headers.get("Authorization")
    print("AUTH HEADER:", auth_header)


    if auth_header is None:
        request.state.user = None
        return await call_next(request)


    try:

        token = auth_header.split(" ")[1]
        print("TOKEN:", token)

        data = verify_token(token)
        print("TOKEN DATA:", data)

        request.state.user = data


    except Exception as e:
        print("TOKEN ERROR:", e)
        request.state.user = None


    response = await call_next(request)

    return response
'''
@app.middleware("http")
async def auth_middleware(request:Request, call_next):

    request.state.user=None

    token=request.headers.get("Authorization")

    if token:
        token=token.replace("Bearer ","")

        data=verify_token(token)

        request.state.user=data


    response=await call_next(request)

    return response
'''
#create blog
@app.post("/blogs")
def create_blog(
    blog: schemas.BlogCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    print("USER DATA:", user)

    print("BLOG DATA:", blog)


    user_id = user["user_id"]


    category = db.query(models.Category).filter(
        models.Category.id == blog.category_id
    ).first()


    if category is None:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )



    existing_blog = db.query(models.Blog).filter(
        models.Blog.title == blog.title,
        models.Blog.user_id == user_id
    ).first()



    if existing_blog:

        raise HTTPException(
            status_code=400,
            detail="Blog title already exists"
        )



    new_blog = models.Blog(

        title=blog.title,

        content=blog.content,

        user_id=user_id,

        category_id=blog.category_id

    )


    db.add(new_blog)

    db.commit()

    db.refresh(new_blog)



    return {

        "message":"Blog created successfully",

        "blog_id":new_blog.id,

        "title":new_blog.title,

        "category_id":new_blog.category_id,

        "user_id":new_blog.user_id

    }
    '''
@app.post("/categories")
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = models.Category(
        name=category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

#get blogs
@app.get("/blogs")
def get_blogs(
    user = Depends(get_current_user),
    db:Session=Depends(get_db)
):
    user_id = user["user_id"]
    blogs = db.query(models.Blog).filter(
        models.Blog.user_id == user_id
    ).all()   

    return blogs

# Add this to main.py
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_single_blog(id, db = Depends(get_db)):
    # Query the database for the blog matching the ID
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    # If the blog does not exist, throw a 404 error
    if not blog:
        raise HTTPException(
            status_code=404, 
            detail=f"Blog with id {id} was not found"
        )
    return blog

#delete blog
@app.delete("/blogs/{id}")
def delete_blog(
    id:int,
    db:Session=Depends(get_db)
):
    return crud.delete_blog(
        db,
        id
    )