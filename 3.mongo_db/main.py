from fastapi import FastAPI, APIRouter
import uvicorn

from database.db_config import init_db
from contextlib import asynccontextmanager
from routes.user_route import user_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("db 실행")
    yield
    print("db 종료 및 프로그램 종료")
    
app = FastAPI(lifespan=lifespan)
route = APIRouter()
app.include_router(route)
app.include_router(user_route, prefix="/user")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)