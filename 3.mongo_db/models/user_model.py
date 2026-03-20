from beanie import Document
from typing import Optional

class User(Document):
    name: str
    email: str
    pwd: str
    age: Optional[int] = None
    
    class Settings: # MongoDB 컬렉션 이름을 지정하는 부분
        name = "users"
        

