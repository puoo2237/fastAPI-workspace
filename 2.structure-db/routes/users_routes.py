from fastapi import APIRouter, HTTPException, status, Path, Query, Depends, Form
from models.users_models import User, UserSignIn, UserSignUp, UserUpdate
from database.connection import get_session
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token, verify_access_token

user_router = APIRouter(tags=["User"])
hash_password = HashPassword()

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
    token: str=Depends(verify_access_token),
    id:int=Query(1, description="사용자 ID"), 
    session=Depends(get_session)
    )->User:
    # print(f"req token: {token}")
    # re_token = verify_access_token(token)
    print(f"return token: {token}")
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당하는 유저 존재하지 않음"
        )
    return user 

@user_router.put("/put/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
    data: UserUpdate=Form(...),
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
    data: UserSignUp=Form(...), 
    session=Depends(get_session)
    )->dict: 
    
    if session.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="존재하는 email"
        )

    user = User(
        email = data.email,
        password= hash_password.create_hash(),
        name=data.name
    )
    session.add(user)
    session.commit()
    session.refresh(user) # 저장된 데이터 확인
    return {"message": "User created successfully"}

@user_router.post("/signin", status_code=status.HTTP_200_OK)
async def signin_user(
    data: UserSignIn=Form(...), 
    session=Depends(get_session)
    )->dict:
    user = session.query(User).filter(User.email == data.email).first()
    if user:
        if hash_password.verify_hash(data.password, user.password):
            return {
                    "token": create_access_token(data.email), 
                    "type": "bearer"                    }
        else:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="Invalid password"
            )
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Invalid email"
    )
        