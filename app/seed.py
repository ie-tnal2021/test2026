# app/seed.py
"""デモ用のユーザーとタスクを投入する。すでに投入済みなら、何もしない。"""
import os
import sys
from datetime import date, timedelta

from dotenv import load_dotenv
from database.db import SessionLocal, engine
from database.models import Base, User, Paper
from security import get_password_hash

load_dotenv()  # .envのDEMO_EMAIL・DEMO_PASSWORDを読み込む

DEMO_EMAIL = os.environ.get("DEMO_EMAIL")
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD")  # どちらも公開されるAPIに残るので、コードには書かない
if not DEMO_EMAIL or not DEMO_PASSWORD:
    sys.exit("環境変数 DEMO_EMAIL・DEMO_PASSWORD を指定してください（.envを参照）")
Base.metadata.create_all(bind=engine)  # テーブルがなければ作る（あれば何もしない）
db = SessionLocal()
try:
    if db.query(User).filter(User.email == DEMO_EMAIL).first():
        print("デモデータは投入済みです")
    else:
        user = User(email=DEMO_EMAIL, hashed_password=get_password_hash(DEMO_PASSWORD))
        db.add(user)
        db.flush()  # user.id を確定させる（まだコミットはしない）
        today = date.today()
        db.add_all([
            Paper(title="論文1: レポートを書く", done=False, user_id=user.id),
            Paper(title="論文2: 買い物に行く", done=True, published_date=2026, user_id=user.id),
            Paper(title="論文3: Dockerの復習", done=False, user_id=user.id),
        ])
        print("6")
        db.commit()
        print("デモデータを投入しました")
finally:
    db.close()