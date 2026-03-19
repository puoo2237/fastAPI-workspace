**FastAPI 실행**
```
# 직접 실행
python -m uvicorn [file name]:[api name] --port [port] --reload

# ex)
python -m uvicorn ex01:app --port 8000 --reload

# main.py 실행
python main.py
```
- 관련 파일 설치
    ```
    pip install fastapi uvicorn
    pip install "pydantic[email]"
    pip install sqlmodel
    ```
- fastapi docs 접속
    - localhost:[port]/docs

---
**router**
- 방식
    - get
    - put
    - delete
    - post
- 데코레이션
    - @[routerName].[방식]("path", response_model=[출력형태], status_code=[출력상태])

**model**
- DTO 역할
    - 일반적으로 pydentic의 BaseModel을 사용하여 타입 검증
    - sqlmodel과 연동
        - SQLModel
        - Field

**database**
- SQLite 이용
- 연동에 필요한 설정

---
**파라미터 처리 방식**
- Path(/)
    - id:int=Path(..., description="사용자 id")
        - ...: 필수값
        - description: 설명
- Query(?)
    - Query(1, description="사용자 id")
        - 1: default 
        - description: 설명
