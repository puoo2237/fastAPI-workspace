from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from models.users_models import User, UserSignIn, UserSignUp, UserUpdate
from database.connection import get_session

user_router = APIRouter(tags=["User"])

# @user_router.get("/test")
# async def test()->dict:
#     return {"message": "Hello World"}

@user_router.get("/all", status_code=status.HTTP_200_OK)
async def get_users(
    session=Depends(get_session)
    )->list[User]:
    users = session.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="목록이 존재하지 않음"
        )
    return users

@user_router.get("/one", status_code=status.HTTP_200_OK)
async def get_user(
    id:int=Query(1, description="사용자 ID"), 
    session=Depends(get_session)
    )->User:
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당하는 유저 존재하지 않음"
        )
    return user 

@user_router.put("/put/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
    data: UserUpdate,
    id:int=Path(..., description="사용자 ID"),
    session=Depends(get_session)
    ):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당하는 유저 존재하지 않음"
        )
    user.name = data.name if data.name else user.name
    user.password = data.password if data.password else user.password
    session.commit()

@user_router.delete("/del/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id:int=Path(..., description="사용자 ID"),
    session=Depends(get_session)
):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당하는 유저 존재하지 않음"
        )
    session.delete(user)
    session.commit()

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def insert(
    data: UserSignUp, 
    session=Depends(get_session)
    )->dict:
    if session.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="존재하는 email"
        )
    user = User(
        email = data.email,
        password= data.password,
        name=data.name
    )
    session.add(user)
    session.commit()
    session.refresh(user) # 저장된 데이터 확인
    return {"message": "User created successfully"}

@user_router.post("/signin", status_code=status.HTTP_200_OK)
async def signin_user(
    data: UserSignIn, 
    session=Depends(get_session)
    )->dict:
    user = session.query(User).filter(User.email == data.email).first()
    if user:
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
        