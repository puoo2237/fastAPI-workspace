from sqlmodel import SQLModel, Session, create_engine  

database_file = "my-test.db" # sqllite에 저장될 파일(db 파일명)
database_connection_string = f"sqlite:///{database_file}" # sqllite 연결 문자열

# 다중 요청 시 처리
connect_args = {"check_same_thread": False} # sqllite 연결 인자

engine_url = create_engine(
    database_connection_string, 
    echo=True,
    connect_args=connect_args
    ) # 엔진 생성

def conn():
    SQLModel.metadata.create_all(engine_url) # 테이블 생성

def get_session():
    with Session(engine_url) as session:
        yield session