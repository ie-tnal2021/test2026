# app/database/db.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # .envのDATABASE_URLを読み込む（すでに設定されている場合は上書きしない）

DATABASE_URL = os.environ["DATABASE_URL"]  # 未設定ならKeyErrorになる（フォールバックしない）

# PaaSが渡すURLは「postgresql://」（または「postgres://」）の形のため、使うドライバ（psycopg2）を明示した形に書き換える
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# check_same_threadはSQLite専用の設定のため、SQLiteのときだけ渡す
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """リクエストごとにDBセッションを開き、処理が終わったら閉じる依存性関数。

    Yields:
        Session: リクエスト処理中に使うDBセッション。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()