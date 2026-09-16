# week05
## 課題05-1: 自分のドメインへのマイグレーション適用
```
vscode ➜ /workspaces/test2026/week05/paper_api (main) $ git diff
diff --git a/week05/paper_api/alembic.ini b/week05/paper_api/alembic.ini
index 807ded2..4026cbe 100644
--- a/week05/paper_api/alembic.ini
+++ b/week05/paper_api/alembic.ini
@@ -86,7 +86,7 @@ path_separator = os
 # database URL.  This is consumed by the user-maintained env.py script only.
 # other means of configuring database URLs may be customized within the env.py
 # file.
-sqlalchemy.url = driver://user:pass@localhost/dbname
+sqlalchemy.url = sqlite:///.papers.db
 
 
 [post_write_hooks]
diff --git a/week05/paper_api/alembic/env.py b/week05/paper_api/alembic/env.py
index 36112a3..718c38a 100644
--- a/week05/paper_api/alembic/env.py
+++ b/week05/paper_api/alembic/env.py
@@ -16,9 +16,8 @@ if config.config_file_name is not None:
 
 # add your model's MetaData object here
 # for 'autogenerate' support
-# from myapp import mymodel
-# target_metadata = mymodel.Base.metadata
-target_metadata = None
+from database.models import Base
+target_metadata = Base.metadata
 
 # other values from the config, defined by the needs of env.py,
 # can be acquired:
```

## 課題05-2: 異常系テストケースの洗い出し

- リソースが存在しない, 404の例
    - 入力: 存在しないIDへのGET, GET /api/v1/papers/999
    - 期待される応答: 404, detailsに「not found」を含む
- バリデーションエラー, 400 or 422の例
    - 入力: 必須項目を含まないPOST, POST /api/v1/papersに{}
    - 期待される応答: 422, detailにバリデーションエラーの内容
- 重複登録, 409の例
    - 入力: 同じemailで2回ユーザ登録
    - 期待される応答: 409, detailに「already used」を含む
- サーバエラー, 500の例
    - 入力: DB接続断
    - 期待される応答: 500, detailに「db connection lost」を含む
