from fastapi import Request
from auth import verify_token


async def auth_middleware(request: Request, call_next):

    if request.url.path in ["/login", "/signup"]:
        return await call_next(request)


    auth_header = request.headers.get("Authorization")


    if not auth_header:
        request.state.user = None
        return await call_next(request)


    try:

        token = auth_header.split(" ")[1]

        user = verify_token(token)

        request.state.user = user


    except Exception:

        request.state.user = None


    response = await call_next(request)

    return response