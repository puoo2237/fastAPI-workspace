from fastapi import APIRouter, HTTPException, status, Depends
from models.user_model import User
from schemas.user_schema import InputUser, LoginUser, SignUpUser
from auth.jwt_handler import create_access_token, verify_access_token
from auth.hash_password import HashPwd

hashed = HashPwd()

user_route = APIRouter(tags=["User"])

@user_route.get("/all")
async def all_user():
    users = User.find_all()
    return await users.to_list()

@user_route.get("/one/{user_id}")
async def one_user_by_id(user_id:str):
    user = await User.get(user_id)
    if user:
        return user
    return {"msg": "no data"}

@user_route.get("/one/{user_name}")
async def one_user_by_name(user_name:str)->dict:
    user = await User.find_one(User.name == user_name)
    if user:
        return user
    return {"msg": "no data"}

@user_route.post("/insert")
async def insert(data:SignUpUser)->dict:
    data.pwd = hashed.create_hash(data.pwd)
    user = User(**data.model_dump())
    await user.insert()
    return {"id": str(user.id)}

@user_route.post("/login")
async def login(data: LoginUser)->dict:
    user = await User.find_one(User.email == data.email)
    if user:
        if hashed.verity_hash(data.pwd, user.pwd):
            return {
                "token": create_access_token(data.email),
                "type": "bearer"
            }
        else:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="Invalid password"
            )
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Invalid email"
    )   
        

@user_route.delete("/del/{user_name}")
async def del_user(user_name: str)->dict:
    count = await User.find(User.name == user_name).delete()
    return {"msg": f"삭제된 수: {count}"}

@user_route.put("/update/{id}")
async def update_user(
    data: InputUser,
    id: str,
    token:str=Depends(verify_access_token), 
    )->dict:
    print(f"token: {token}")
    user = await User.get(id)
    user.name = data.name
    user.pwd = hashed.create_hash(data.pwd)
    user.age = data.age
    await user.save()
    return {"msg": "수정 성공", "user": user}
