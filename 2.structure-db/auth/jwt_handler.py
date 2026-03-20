import time
from datetime import datetime
from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError

SECRET_KEY = "아무값이나 처리"
api_key_header = APIKeyHeader(name="Authorization")

def create_access_token(email:str) -> str:
    payload = {
        "sub": email,
        "expires": time.time() + 20 # 만료시간
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") # token = 헤더.페이로드.서명
    print(f"token: {token}, type: {type(token)}")
    return token

def verify_access_token(token:str=Security(api_key_header))->str:
    # print(f"verity access token: {token}")
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="로그인 먼저 하세요."
            )
        if datetime.now() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="토큰 만료"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    return "내용 확인"
    