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
    pip install fastapi uvicorn "pydantic[email]" sqlmodel 
    pip install bcrypt python-jose[cryptography] python-multipart 
    pip install beanie motor
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
- DB
    - 모든 목록 확인
        - session.query([테이블]).all()
    - 특정 목록 확인
        - session.get([테이블], [id])
        - session.query([테이블]).filter([조건]).first
    - 추가
        - session.add([데이터])
    - 삭제
        - 목록 가져온 후 session.delete()
    - 수정
        - 목록의 가져온 후 수정
    - 반영
        - session.commit()
    - 취소
        - session.rollback()
    - 연결 종료 
        - session.close()
    - 재조회
        - session.refresh()

**model**
- DTO 역할
    - BaseModel
        - 데이터 검증 (validation)
        - 타입 체크
        - 직렬화(JSON 변환)
    - Document(BaseModel + DB 기능)
        - MongoDB 컬렉션과 연결된 모델 
        - BaseModel을 내부적으로 상속함
        - 실제 DB에 저장됨
    - sqlmodel과 연동
        - SQLModel
        - Field

**database**
- 연동에 필요한 설정
- 종류
    - SQLite
    - MongoDB
        - 개념
            - DB = 데이터베이스
            - Collection = 테이블 같은 개념
            - Document = JSON 객체
        - 문법
            - 조회
                ```
                db.users.find()
                db.users.find({ age: 25 })
                db.users.findOne({ name: "철수" })
                db.users.find({
                                age: { $gt: 20 },
                                name: "철수"
                                })
                db.users.find({
                                $or: [
                                    { age: 25 },
                                    { name: "영희" }
                                ]
                                })
                db.users.find().limit(2)
                db.users.find({}, { name: 1, _id: 0 })
                db.users.find().sort({ age: 1 })   // 오름차순
                db.users.find().sort({ age: -1 })  // 내림차순
                ```
            - 조건
                ```
                db.users.find({ age: { $gt: 20 } })   // >
                db.users.find({ age: { $lt: 30 } })   // <
                db.users.find({ age: { $gte: 25 } })  // >=
                ```
            - 업데이트
                ```
                db.users.updateOne(
                                    { name: "철수" },
                                    { $set: { age: 26 } }
                                    )
                db.users.updateMany(
                                    { age: { $gt: 20 } },
                                    { $set: { status: "active" } }
                                    )
                ```   
            - 삭제
                ```
                db.users.deleteOne({ name: "철수" })
                db.users.deleteMany({ age: { $lt: 20 } })
                db.users.deleteMany({})
                db.users.drop()
                ``` 
            - 추가
                ```
                db.users.insertOne({name:"홍길동", age:20})
                db.users.insertMany([{name:"홍당무", age:23}, {name:"김구라",age:50}])
                ```
            - 기타
                ```
                show dbs
                use mydatabase
                db.createCollection("users")
                show collections
                ```

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

