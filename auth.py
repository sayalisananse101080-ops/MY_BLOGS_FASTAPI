from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import HTTPException

SECRET_KEY="my_blog_secret_key"
ALGORITHM="HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
#password hash
def hash_password(password):
    return pwd_context.hash(password)
#password verify
def verify_password(password,hashed):
    return pwd_context.verify(
        password,
        hashed
    )
#create JWT token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode["exp"] = expire

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

#verify JWT tokens
def verify_token(token:str):
    try:
        data=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return data
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )