from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer
from auth import verify_token


security = HTTPBearer()


def get_current_user(
    credentials = Security(security)
):

    token = credentials.credentials


    data = verify_token(token)


    if "user_id" not in data:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    return data