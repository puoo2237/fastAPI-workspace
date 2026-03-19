from fastapi import APIRouter, HTTPException, status
from models.users_models import User, UserSignIn

user_router = APIRouter(tags=["User"])

users = []

@user_router.get("/test")
async def test()->dict:
    return {"message": "Hello World"}

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def insert(data: User)->dict:
    if any(user.email == data.email for user in users):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="존재하는 email"
        )
    users.append(data)
    return {"message": "User created successfully"}

@user_router.post("/signin", status_code=status.HTTP_200_OK)
async def signin_user(data: UserSignIn)->dict:
    for user in users:
        if user.email == data.email:
            if user.password == data.password:
                return {"message": "Signin successful"}
            else:
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password"
                )
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Invalid email"
    )
        