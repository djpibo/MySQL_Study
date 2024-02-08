from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/solodb"

engine = create_engine(DATABASE_URL, echo=True)  # echo : 처리된 쿼리를 print 해주는 옵션
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
