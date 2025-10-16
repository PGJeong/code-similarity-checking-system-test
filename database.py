from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# 환경 변수 주입
DATABASE_URL = settings.DATABASE_URL

# 데이터베이스 초기화 설정
print(f"[DEBUG] Connecting to database: {DATABASE_URL}")  # 디버깅용 출력
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
