from pydantic import BaseModel, EmailStr

class InputUser(BaseModel):
    name: str
    pwd: str
    age: int | None = None

class SignUpUser(BaseModel):
    name: str
    email: EmailStr
    pwd: str
    age: int | None = None
    
class LoginUser(BaseModel):
    email: EmailStr
    pwd: str
    