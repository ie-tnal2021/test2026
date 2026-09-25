# tests/conftest.py（テスト用DB分離）
import pytest  # pytest自体のAPI（@pytest.fixture()等）を使うために必要
from sqlalchemy import create_engine  # DBへの接続方法を表すengineを作る（第5回参照）
from sqlalchemy.orm import sessionmaker  # セッションを作るための工場を作る（第5回参照）
from database.models import Base
from database.db import get_db
from main import app
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture()
def client():
    """テスト専用DBを使うTestClientを返すfixture。

    テスト実行前にテスト専用DB（test.db）にテーブルを作成し、アプリのget_dbを
    テスト用DBのセッションに差し替える。テスト終了後にテーブルを削除する。

    Yields:
        TestClient: 差し替え済みのアプリに、直接リクエストを送るクライアント。
    """
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def auth_headers(client):
    """認証済みのリクエストに付けるAuthorizationヘッダを返すfixture。

    テスト専用DBにユーザ（test@example.com）を登録・ログインし、
    取得したトークンでヘッダを作る。

    Args:
        client: テスト専用DBを使うTestClient（上のclient fixture）。

    Returns:
        dict: {"Authorization": "Bearer <トークン>"}
    """
    client.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "testpass123"})
    response = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "testpass123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}