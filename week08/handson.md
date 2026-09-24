# 意図的に脆弱なコードへの攻撃実演（自作＋AI生成の両方）
## ステップ1: 自作の脆弱なエンドポイントを一時的に作る
コピペでエンドポイント実装。

## ステップ2: 動作確認（攻撃が成功することを確認する）
- TOKEN_A, TOKEN_B 2ユーザのトークン取得するところまでを `source setup_tokens.sh` で用意。
- TOKEN_A, TOKEN_B どちらからでも双方の検索結果に全てのタスクが含まれることを確認。
```
(base) oct2026:tnal% source setup_tokens.sh
(base) oct2026:tnal% curl -H "Authorization: Bearer $TOKEN_A" "http://localhost:8000/api/v1/debug/tasks-search?q=x%27%20OR%20%271%27%3D%271%27%20--%20"
[{"id":1,"title":"task userB","done":0,"due_date":null,"created_at":"2026-09-24 03:23:59","user_id":2},{"id":2,"title":"task userA","done":0,"due_date":null,"created_at":"2026-09-24 03:24:06","user_id":1},{"id":3,"title":"task userA 2","done":0,"due_date":null,"created_at":"2026-09-24 03:24:12","user_id":1}]
(base) oct2026:tnal% curl -H "Authorization: Bearer $TOKEN_B" "http://localhost:8000/api/v1/debug/tasks-search?q=x%27%20OR%20%271%27%3D%271%27%20--%20"
[{"id":1,"title":"task userB","done":0,"due_date":null,"created_at":"2026-09-24 03:23:59","user_id":2},{"id":2,"title":"task userA","done":0,"due_date":null,"created_at":"2026-09-24 03:24:06","user_id":1},{"id":3,"title":"task userA 2","done":0,"due_date":null,"created_at":"2026-09-24 03:24:12","user_id":1}]
```

## ステップ3: コーディングエージェントに同じエンドポイントを安全に実装し直させる
### gemini 挙動確認
```
Fixing vulnerable tasks-search endpoint: 
  I will rewrite the `/api/v1/debug/tasks-search` endpoint in `main.py` to use a parameterized SQLAlchemy
  query for secure partial matching, replacing the vulnerable string interpolation.

╭────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ? Edit  main.py: @app.get("/api/v1/debug/tasks-... => @app.get("/api/v1/debug/tasks-...                    │
│ ╭────────────────────────────────────────────────────────────────────────────────────────────────────────╮ │
│ │ 108                                                                                                    │ │
│ │ 109   # 演習用（本番には絶対に入れない）: 文字列結合のSQL                                              │ │
│ │ 110   @app.get("/api/v1/debug/tasks-search")                                                           │ │
│ │ 111 - def search_tasks_vulnerable(                                                                     │ │
│ │ 111 + def search_tasks(                                                                                │ │
│ │ 112       q: str,                                                                                      │ │
│ │ 113       db: Session = Depends(get_db),                                                               │ │
│ │ 114       current_user: db_models.User = Depends(get_current_user),                                    │ │
│ │ 115   ):                                                                                               │ │
│ │ 116       from sqlalchemy import text                                                                  │ │
│ │ 117 -     result = db.execute(text(f"SELECT * FROM tasks WHERE title LIKE '%{q}%'"))                   │ │
│ │ 117 +     # Parameterized query to avoid SQL injection and filter by user_id                           │ │
│ │ 118 +     stmt = text("SELECT * FROM tasks WHERE title LIKE :title AND user_id = :user_id")            │ │
│ │ 119 +     result = db.execute(stmt, {"title": f"%{q}%", "user_id": current_user.id})                   │ │
│ │ 120       return [dict(row._mapping) for row in result]                                                │ │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                                                         │
```
- 関数名を search_tasks に変更: ok
- f-stringによる文字列結合から、プレースホルダ＋バインドパラメータ方式に変更: ok

```
Concluding endpoint refactor: 
  I am concluding the task after successfully refactoring the `/api/v1/debug/tasks-search` endpoint to use
  secure parameterized queries and implementing user-based filtering.


✦ I have successfully refactored the /api/v1/debug/tasks-search endpoint in main.py.

  The changes made:
   - Replaced the vulnerable f-string SQL query (SELECT * FROM tasks WHERE title LIKE '%{q}%') with a
     parameterized query using SQLAlchemy's text and parameter binding (:title).
   - Added filtering by user_id (AND user_id = :user_id) to ensure that users can only search their own tasks,
     maintaining security best practices alongside the authentication dependency.
   - Kept the Depends(get_current_user) dependency intact as requested.
```

実装終了報告。

- チェック項目
    - filter(Task.title.contains(q)) のようなORMメソッドを使っているか、それとも文字列結合を使っていないか => ok
    - main.py内に/api/v1/debug/tasks-searchのルートが1つだけになっているか => OK
    - Depends(get_current_user)がそのまま残っているか => OK

## ステップ4: 動作確認（攻撃が失敗することを確認する）
### 動作確認
```
(base) oct2026:tnal% curl -H "Authorization: Bearer $TOKEN_A" "http://localhost:8000/api/v1/debug/tasks-search?q=x%27%20OR%20%271%27%3D%271%27%20--%20"
[]
(base) oct2026:tnal% curl -H "Authorization: Bearer $TOKEN_B" "http://localhost:8000/api/v1/debug/tasks-search?q=x%27%20OR%20%271%27%3D%271%27%20--%20"
[]
(base) oct2026:tnal% curl -H "Authorization: Bearer $TOKEN_A" "http://localhost:8000/api/v1/tasks/"
(base) oct2026:tnal% curl -H "Authorization: Bearer $TOKEN_A" "http://localhost:8000/api/v1/tasks"
[{"id":2,"title":"task userA","done":false,"due_date":null,"created_at":"2026-09-24T03:24:06"},{"id":3,"title":"task userA 2","done":false,"due_date":null,"created_at":"2026-09-24T03:24:12"}]
```

SQLiが効かなくなっている。
