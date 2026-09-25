# tests/test_ai_generated.py
# --- 第6回: 検索フィルタ（q） ---
def test_search_returns_only_matching_titles(client, auth_headers):
    """qに部分一致するタイトルのタスクだけが返る。"""
    client.post("/api/v1/tasks", json={"title": "牛乳を買う"}, headers=auth_headers)
    client.post("/api/v1/tasks", json={"title": "レポートを書く"}, headers=auth_headers)
    response = client.get("/api/v1/tasks", params={"q": "レポート"}, headers=auth_headers)
    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["レポートを書く"]


def test_search_can_be_combined_with_done(client, auth_headers):
    """qとdoneを併用すると、両方の条件（AND）に一致するタスクだけが返る。"""
    client.post("/api/v1/tasks", json={"title": "レポートA", "done": True}, headers=auth_headers)
    client.post("/api/v1/tasks", json={"title": "レポートB", "done": False}, headers=auth_headers)
    response = client.get("/api/v1/tasks", params={"q": "レポート", "done": True}, headers=auth_headers)
    assert [t["title"] for t in response.json()] == ["レポートA"]


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


def test_tasks_without_token_returns_401(client):
    """トークンなしで保護されたエンドポイントを呼ぶと、401になる。"""
    assert client.get("/api/v1/tasks").status_code == 401


# --- 第8回: 脆弱性の修正（SQLインジェクション） ---
def test_search_is_not_vulnerable_to_sql_injection(client, auth_headers):
    """SQLの断片をqに渡しても、全件は取得できず、文字列として扱われる。"""
    client.post("/api/v1/tasks", json={"title": "牛乳を買う"}, headers=auth_headers)
    response = client.get("/api/v1/tasks", params={"q": "x' OR '1'='1' -- "}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []