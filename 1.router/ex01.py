from fastapi import FastAPI, APIRouter, Path, Query, HTTPException, status
from PackBook import User

app = FastAPI(title="TEST FASTAPI",
              description="fastapi example",
              version="1.0.0")

router = APIRouter()

users = []

@router.get("/test")
async def test() -> dict:
    return {"msg": "test msg"}

@router.post("/insert")
async def insert(user: User) -> dict:
    print(user)
    users.append(user)
    return {"msg": "데이터 추가 성공"}

@router.get("/select", response_model=list[User])
async def select() -> list[User]:
    return users

@router.get("/path/{id}",
    responses={
        200: { "description": "successfully",
            "content": {
                "application/json": { "example": {"id": 1, "name": "홍길동"} }
            },
        },
        404: { "description": "User not found",
            "content": {
                "application/json": { "example": {} }
            },
        },
})
async def get_one(id:int) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {"msg": "데이터를 찾을 수 없습니다."}

@router.get("/path2/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_one2(id:int=Path(..., description="사용자 id")) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {"msg": "데이터를 찾을 수 없습니다."}

@router.get("/query")
async def get_query(id:int=Query(1, description="사용자 id")) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return {"msg": "데이터를 찾을 수 없습니다."}


@router.put("/update/{id}", status_code=200)
async def update(u: User, id:int)->dict:
    for user in users:
        if user.id == id:
            user.name=u.name
            return {"msg": "데이터 수정 성공"}
    raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK
               )
async def del_all()->dict:
    users.clear()
    return {"msg": "데이터 전체 삭제 성공"} 

app.include_router(router)