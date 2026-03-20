from time import time
from datetime import datetime
from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError

SECRET_KEY = "몽고"
api_key_header = APIKeyHeader(name="Authorization")

def create_access_token(email:str)->str:
    payload = {
        "sub": email,
        "expire": time() + 60
    }
    token = jwt.encode(
        claims=payload,
        key=SECRET_KEY,
        algorithm="HS256"
        )
    return token

def verify_access_token(token:str=Security(api_key_header))->str:
    try:
        de_token = jwt.decode(
            token = token, 
            key= SECRET_KEY,
            algorithms="HS256"
            )
        expire = de_token.get("expire")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="login first"
            )
        if datetime.now() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Expired token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )