# tests/test_tasks.py
def test_list_tasks_empty(client, auth_headers):
    """タスクが1件もないとき、一覧は空のリストになる。"""
    response = client.get("/api/v1/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_task(client, auth_headers):
    """作成したタスクを、返ってきたIDで取得できる。"""
    created = client.post("/api/v1/tasks", json={"title": "買い物"}, headers=auth_headers).json()
    response = client.get(f"/api/v1/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "買い物"

def test_create_task_validation_error(client, auth_headers):
    """titleが空文字のときは、バリデーションエラー（422）になる。"""
    response = client.post("/api/v1/tasks", json={"title": ""}, headers=auth_headers)
    assert response.status_code == 422

def test_create_and_update_task(client, auth_headers):
    """作成したタスクを、返ってきたIDで更新できる。"""
    created = client.post("/api/v1/tasks", json={"title": "買い物"}, headers=auth_headers).json()
    updated = client.patch(f"/api/v1/tasks/{created['id']}",json={"done": True}, headers=auth_headers)
    assert updated.status_code == 200
    assert updated.json()["title"] == "買い物"
    assert updated.json()["done"] == True
    response = client.get(f"/api/v1/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "買い物"
    assert response.json()["done"] == True
