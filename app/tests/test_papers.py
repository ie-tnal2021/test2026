# tests/test_papers.py
from jose import jwt
import main

import importlib
import pytest

def test_list_papers_empty(client, auth_headers):
    """タスクが1件もないとき、一覧は空のリストになる。"""
    response = client.get("/api/v1/papers", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_paper(client, auth_headers):
    """作成したタスクを、返ってきたIDで取得できる。"""
    created = client.post("/api/v1/papers", json={"title": "論文1"}, headers=auth_headers).json()
    response = client.get(f"/api/v1/papers/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "論文1"

def test_create_paper_validation_error(client, auth_headers):
    """titleが空文字のときは、バリデーションエラー（422）になる。"""
    response = client.post("/api/v1/papers", json={"title": ""}, headers=auth_headers)
    assert response.status_code == 422

# tests/test_ai_generated.py
# --- 第6回: 検索フィルタ（q） ---
def test_search_returns_only_matching_titles(client, auth_headers):
    """qに部分一致するタイトルのタスクだけが返る。"""
    client.post("/api/v1/papers", json={"title": "論文1: 牛乳を買う"}, headers=auth_headers)
    client.post("/api/v1/papers", json={"title": "論文2: レポートを書く"}, headers=auth_headers)
    response = client.get("/api/v1/papers", params={"q": "レポート"}, headers=auth_headers)
    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["論文2: レポートを書く"]


def test_search_can_be_combined_with_done(client, auth_headers):
    """qとdoneを併用すると、両方の条件（AND）に一致するタスクだけが返る。"""
    client.post("/api/v1/papers", json={"title": "論文1: レポートA", "done": True}, headers=auth_headers)
    client.post("/api/v1/papers", json={"title": "論文2: レポートB", "done": False}, headers=auth_headers)
    response = client.get("/api/v1/papers", params={"q": "レポート", "done": True}, headers=auth_headers)
    assert [t["title"] for t in response.json()] == ["論文1: レポートA"]


# --- 第7回: 認証 ---
def test_register_duplicate_email_returns_409(client):
    """同じメールアドレスで2回登録すると、2回目は409になる。"""
    body = {"email": "dup@example.com", "password": "testpass123"}
    assert client.post("/api/v1/auth/register", json=body).status_code == 201
    assert client.post("/api/v1/auth/register", json=body).status_code == 409


def test_login_with_wrong_password_returns_401(client):
    """パスワードが違うと、ログインは401になる。"""
    client.post("/api/v1/auth/register", json={"email": "a@example.com", "password": "testpass123"})
    response = client.post("/api/v1/auth/login", json={"email": "a@example.com", "password": "wrong-password"})
    assert response.status_code == 401


def test_papers_without_token_returns_401(client):
    """トークンなしで保護されたエンドポイントを呼ぶと、401になる。"""
    assert client.get("/api/v1/papers").status_code == 401


# --- 第8回: 脆弱性の修正（SQLインジェクション） ---
def test_search_is_not_vulnerable_to_sql_injection(client, auth_headers):
    """SQLの断片をqに渡しても、全件は取得できず、文字列として扱われる。"""
    client.post("/api/v1/papers", json={"title": "論文1: 牛乳を買う"}, headers=auth_headers)
    response = client.get("/api/v1/papers", params={"q": "x' OR '1'='1' -- "}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

# 登録時email未設定時の挙動チェック
def test_no_email(client):
    """email指定無しだと、ログインは401になる。"""
    body = {"email": "", "password": "testpass123"}
    response = client.post("/api/v1/auth/register", json=body)
    assert response.status_code == 422

def test_token_without_sub_returns_401(client):
    """署名は正しいが、sub（ユーザーの識別子）がないトークンは、401になる。"""
    token = jwt.encode({"foo": "bar"}, main.SECRET_KEY, algorithm=main.ALGORITHM)
    response = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_missing_secret_key_raises_error(monkeypatch):
    """SECRET_KEY未設定ならエラーになる"""
    monkeypatch.delenv("SECRET_KEY", raising=False)                  # 環境変数を消す
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **k: None)  # .envも読まない
    with pytest.raises(SystemExit):
        importlib.reload(main)                                   # 読み込み直す