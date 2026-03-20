import motor.motor_asyncio
from beanie import init_beanie
from models.user_model import User

MONGODB_URL = "mongodb://localhost:27017"

async def init_db():
    # db와 fastapi 연동
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    database = client.mydatabase # db 생성
    
    await init_beanie(database=database, document_models=[User])