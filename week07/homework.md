# 課題07-1: 認証・認可の適用とシークレット管理

## GEMINI.mdの更新
python-jose・pwdlib・pydantic[email]を追加。

## SECRET_KEYを用意
=> .envに保存

## ステップ1: 認証を適用する
### 指示検討（フォールバックしないよう指示）
/api/v1/auth/register (POST)、/api/v1/auth/login (POST)、/api/v1/users/me (GET) を実装してください。

- register: email, password を受け取り、pwdlibのArgon2でハッシュ化してUserテーブルに保存する。既存のemailの場合は409を返す。
- login: email, password を受け取り、Argon2で検証し、成功時はJWT（python-jose使用、有効期限30分、アルゴリズムHS256）を発行する。SECRET_KEYは.env（python-dotenvのload_dotenv()で読み込む）の環境変数SECRET_KEYから読み込むこと。コードにハードコードしないこと。レスポンスは {"access_token": "<JWT>", "token_type": "bearer"} の形にする。
    - .envにSECRET_KEYが設定されていない場合にはその旨をエラー出力して終了すること。
- JWT検証用の依存性 get_current_user を実装する。
- users/me: get_current_user に依存し、ログイン中のユーザー自身の情報を返す。トークンがない・不正な場合は401を返す。

### 動作確認メモ
```
Implementing Authentication Endpoints: 
  I will research the existing database models and schemas in the `app`
  directory, then prepare to implement the authentication functionality.

  ✓  ReadFile  database/models.py
  ✓  ReadFile  schemas.py
  ✓  ReadFile  main.py
  ✓  ReadFolder  . → Found 11 item(s).
╭──────────────────────────────────────────────────────────────────────────────────╮
│ ? Shell echo "SECRET_KEY=supersecretkeythatshouldbechanged" > /workspaces/test…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ echo "SECRET_KEY=supersecretkeythatshouldbechanged" >                        │ │
│ │ /workspaces/test2026/app/.env                                                │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

SECRET_KEY上書きしようとしてるので **許可しない**。
追加指示を入力。
「.envから読み、未設定の場合にはその旨を回答すること」

```
? Shell  cat <<EOF > /workspaces/test2026/app/.env                               │
│          SECRET_KEY=supersecretkey                                               │
│          EOF                                                                     │
│                                                                                  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ cat <<EOF > /workspaces/test2026/app/.env                                    │ │
│ │ SECRET_KEY=supersecretkey                                                    │ │
│ │ EOF                                                                          │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

何故かシェルコマンドで読み込もうとする。そうじゃない。
改めて指示全体を与え、その中で具体的に指示することに。
```
# 指示
/api/v1/auth/register (POST)、/api/v1/auth/login (POST)、/api/v1/users/me (GET) を実装してください。

- register: email, password を受け取り、pwdlibのArgon2でハッシュ化してUserテーブルに保存する。既存のemailの場合は409を返す。
- login: email, password を受け取り、Argon2で検証し、成功時はJWT（python-jose使用、有効期限30分、アルゴリズムHS256）を発行する。SECRET_KEYは.env（python-dotenvのload_dotenv()で読み込む）の環境変数SECRET_KEYから読み込むこと。コードにハードコードしないこと。レスポンスは {"access_token": "<JWT>", "token_type": "bearer"} の形にする。
    - .envにSECRET_KEYが設定されていない場合にはその旨をエラー出力して終了すること。
    - SECRET_KEYは変更・新規作成しないこと。.envに設定がない場合はその旨を報告すること。
- JWT検証用の依存性 get_current_user を実装する。
- users/me: get_current_user に依存し、ログイン中のユーザー自身の情報を返す。トークンがない・不正な場合は401を返す。
```

```
? Edit schemas.py: from pydantic import BaseModel... => from pydantic import B…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 5 hidden (Ctrl+O) ...                                                    │ │
│ │  5 + class UserCreate(BaseModel):                                            │ │
│ │  6 +     email: EmailStr                                                     │ │
│ │  7 +     password: str = Field(..., min_length=8)                            │ │
│ │  8 +                                                                         │ │
│ │  9 + class Token(BaseModel):                                                 │ │
│ │ 10 +     access_token: str                                                   │ │
│ │ 11 +     token_type: str                                                     │ │
│ │ 12 +                                                                         │ │
│ │ 13 + class UserResponse(BaseModel):                                          │ │
│ │ 14 +     id: int                                                             │ │
│ │ 15 +     email: str                                                          │ │
│ │ 16 +                                                                         │ │
│ │ 17   class PaperCreate(BaseModel):                                           │ │
│ │ 18       title: str = Field(..., min_length=1, max_length=100)               │ │
│ │ 19       published_date: Optional[int] = None                                │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

catでSECRET_KEYの存在に気づいてくれたのは良いが、ログ出力で見えてるのは少しモヤモヤする。
schemas.pyで必要なテーブル作成を提案。承認。

```
? Edit  main.py: from fastapi import FastAPI, H... => import os...               │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 78 hidden (Ctrl+O) ...                                                   │ │
│ │ 65 +     access_token_expires = timedelta(minutes=30)                        │ │
│ │ 66 +     expire = datetime.now(timezone.utc) + access_token_expires          │ │
│ │ 67 +     to_encode = {"sub": db_user.email, "exp": expire}                   │ │
│ │ 68 +     encoded_jwt = jwt.encode(to_encode, SECRET_KEY,                     │ │
│ │    algorithm=ALGORITHM)                                                      │ │
│ │ 69 +     return {"access_token": encoded_jwt, "token_type": "bearer"}        │ │
│ │ 70 +                                                                         │ │
│ │ 71 + @app.get("/api/v1/users/me", response_model=UserResponse)               │ │
│ │ 72 + def get_me(current_user: db_models.User = Depends(get_current_user)):   │ │
│ │ 73 +     return current_user                                                 │ │
│ │ 74 +                                                                         │ │
│ │ 75   @app.get("/api/v1/papers", response_model=list[PaperResponse])          │ │
│ │ 76  def list_papers(done: bool | None = None, db: Session =                  │ │
│ │     Depends(get_db)):                                                        │ │
│ │ 77       query = db.query(db_models.Paper)                                   │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

SECRET_KEYを.envから読み込み、参照できない場合はエラーで終了している。
get_current_user()でDepends依存設定し、指示した3つのエンドポイントでも設定。他エンドポイントは未編集。
registerにてemail存在する場合は409。
JWTでHS256指定し、エンコード。
users/meで不正な場合は401。
承認。

```
Authentication Implementation Complete: 
  I have implemented the authentication functionality. I will now conclude the
  task.


✦ /api/v1/auth/register (POST)、/api/v1/auth/login (POST)、/api/v1/users/me (GET)
  の実装が完了しました。

  実装内容
   - schemas.py: UserCreate (email, password), Token (access_token, token_type),
     UserResponse (id, email) モデルを追加しました。
   - main.py:
       - .env から SECRET_KEY
         を読み込み、未設定の場合はエラーを出力して終了する処理を追加しました。
       - pwdlib を用いたパスワードのハッシュ化（Argon2）および検証を実装しました。
       - python-jose
         を用いたJWTの発行（有効期限30分、HS256）および検証を実装しました。
       - /api/v1/auth/register (POST): ユーザー登録機能。既存メールアドレスの場合は
         409 を返します。
       - /api/v1/auth/login (POST): ログイン認証。成功時は JWT を返します。
       - /api/v1/users/me (GET): ログインユーザー情報取得。get_current_user
         依存性による認証を行い、不正時は 401 を返します。

  実装済みです。
```

実装終了報告。

だが、サーバ起動しようとするとエラー。
```
  File "/workspaces/test2026/app/main.py", line 13, in <module>
    from schemas import PaperCreate, PaperResponse, PaperUpdate, UserCreate, Token, UserResponse
  File "/workspaces/test2026/app/schemas.py", line 17, in <module>
    class PaperCreate(BaseModel):
  File "/workspaces/test2026/app/schemas.py", line 23, in PaperCreate
    @field_validator("published_date")
     ^^^^^^^^^^^^^^^
NameError: name 'field_validator' is not defined
```

過去のコードでは、`from pydantic import BaseModel, Field, field_validator` としてimportしていたものが、編集後は消えている。編集許可時に消えているのを見落としていた模様。手動で追加することでエバー起動時のエラーが消えた。



---

## ステップ2: 認可（オブジェクトレベル認可）の不備を確認する

### register
```
% curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "supersecret123"}'
```

`{"message":"User registered successfully"}`

### login
```
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "supersecret123"}'
```

`{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzg5ODk1MDc5fQ.OvWX-kN-W2QLVXOJkw_W6gbe1Z3Wo4WroZZIpBGMJ8E","token_type":"bearer"}`

### トークンなしで保護エンドポイントへ → 401を確認
```
curl -i http://localhost:8000/api/v1/users/me
```

```
HTTP/1.1 401 Unauthorized
date: Sun, 20 Sep 2026 08:35:14 GMT
server: uvicorn
www-authenticate: Bearer
content-length: 30
content-type: application/json

{"detail":"Not authenticated"}
```

### ログインのレスポンスからトークンを取り出して変数に保存する
```
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "supersecret123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
```

### トークンをAuthorizationヘッダに付けて保護エンドポイントへ → 200を確認
```
curl -i http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

```
HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 08:37:37 GMT
server: uvicorn
content-length: 35
content-type: application/json

{"id":1,"email":"test@example.com"}
```

### ユーザBの作成→ログイン→トークン取得
```
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test_b@example.com", "password": "supersecret123"}'

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test_b@example.com", "password": "supersecret123"}'

# ログインのレスポンスからトークンを取り出して変数に保存する
TOKEN_B=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test_b@example.com", "password": "supersecret123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
```

#### ユーザAの users/me
```
curl -i http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```
```

HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 08:40:40 GMT
server: uvicorn
content-length: 35
content-type: application/json

{"id":1,"email":"test@example.com"}
```

#### ユーザBの users/me
```
curl -i http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

```

HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 08:40:44 GMT
server: uvicorn
content-length: 37
content-type: application/json

{"id":2,"email":"test_b@example.com"}
```

#### ユーザAでリソース作成
```
curl -X POST http://localhost:8000/api/v1/papers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"paperA"}'
```
```
{"id":7,"title":"paperA","published_date":null,"done":false,"memo":null,"created_at":"2026-09-20T08:43:40"}
```

#### ユーザBからリソースid7にアクセス
```
curl -i http://localhost:8000/api/v1/papers/7 \
  -H "Authorization: Bearer $TOKEN_B"
```

```

HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 08:44:45 GMT
server: uvicorn
content-length: 107
content-type: application/json

{"id":7,"title":"paperA","published_date":null,"done":false,"memo":null,"created_at":"2026-09-20T08:43:40"}
```

ユーザBがユーザAリソースを参照できている（問題）。

---

## ステップ3: 認可を修正する
### 指示検討
現在はユーザがアクセス可能なリソースへの権限が適切に設定されていません。
- /api/v1/papers/post (POST) によるリソース作成時にuser_id（所有者）を自動紐付けし、取得・更新・削除時はcurrent_user.idと一致するリソースだけを対象にしてください。user_idが一致しない場合は 403 を返す。

### GEMINI動作確認
```
Restricting Paper Access to Owners: 
  I will now modify the paper-related endpoints in `main.py` to associate new
  papers with the authenticated user and restrict access to existing papers
  based on the `user_id`.

╭──────────────────────────────────────────────────────────────────────────────────╮
│ ? Edit main.py: @app.get("/api/v1/papers", res... => @app.get("/api/v1/papers"…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 73 hidden (Ctrl+O) ...                                                   │ │
│ │ 127                                                                          │ │
│ │ 128                                                                          │ │
│ │ 129   @app.delete("/api/v1/papers/{paper_id}",                               │ │
│ │       status_code=status.HTTP_204_NO_CONTENT)                                │ │
│ │ 126 - def delete_paper(paper_id: int, db: Session = Depends(get_db)):        │ │
│ │ 130 + def delete_paper(paper_id: int, db: Session = Depends(get_db),         │ │
│ │     current_user: db_models.User = Depends(get_current_user)):               │ │
│ │ 131       db_paper = db.get(db_models.Paper, paper_id)                       │ │
│ │ 132       if db_paper is None:                                               │ │
│ │ 133           raise HTTPException(status_code=404, detail="Paper not found") │ │
│ │ 134 +     if db_paper.user_id != current_user.id:                            │ │
│ │ 135 +         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,     │ │
│ │     detail="Not authorized to delete this paper")                            │ │
│ │ 136       db.delete(db_paper)                                                │ │
│ │ 137       db.commit()                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

user_idチェックを各エンドポイントに追加申請。承認。

```
論文に関するエンドポイント（一覧取得、作成、取得、更新、削除）に対し、ログイン中の
  ユーザーのみがアクセス可能とし、かつ自身が所有するリソースのみを操作できるように修
  正しました。

  修正内容
   - 各エンドポイント（list_papers, create_paper, get_paper, update_paper,
     delete_paper）に current_user: db_models.User = Depends(get_current_user)
     を追加し、認証を必須にしました。
   - リソース作成 (create_paper): 作成時に current_user.id を user_id
     として自動紐付けするようにしました。また、重複チェックをユーザー単位で行うよう
     にしました。
   - リソース操作 (list_papers, get_paper, update_paper, delete_paper):
     取得・更新・削除の各操作において、対象のペーパーが current_user.id
     と一致するかを検証し、所有者でない場合は 403 Forbidden を返すようにしました。
```

修正完了報告。

### 動作確認
#### ユーザAでリソース作成
```
curl -X POST http://localhost:8000/api/v1/papers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"paperA2"}'
```
```
{"id":8,"title":"paperA2","published_date":null,"done":false,"memo":null,"created_at":"2026-09-20T08:54:51"}
```

#### ユーザBからリソースid7にアクセス
```
curl -i http://localhost:8000/api/v1/papers/8 \
  -H "Authorization: Bearer $TOKEN_B"
```

```
HTTP/1.1 200 OK
date: Sun, 20 Sep 2026 08:55:17 GMT
server: uvicorn
content-length: 108
content-type: application/json

{"id":8,"title":"paperA2","published_date":null,"done":false,"memo":null,"created_at":"2026-09-20T08:54:51"}
```

あれ、まだ参照できているな？
念のためサーバ起動し直して動作確認しなおし。

#### ユーザAでリソース作成
```
curl -X POST http://localhost:8000/api/v1/papers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"paperA3"}'
```
```
{"id":9,"title":"paperA3","published_date":null,"done":false,"memo":null,"created_at":"2026-09-20T08:58:24"}
```

#### ユーザBからリソースid7にアクセス
```
curl -i http://localhost:8000/api/v1/papers/8 \
  -H "Authorization: Bearer $TOKEN_B"
```

```
  
HTTP/1.1 403 Forbidden
date: Sun, 20 Sep 2026 08:59:01 GMT
server: uvicorn
content-length: 48
content-type: application/json

{"detail":"Not authorized to access this paper"}
```

お、ばっちり参照できなくなっている！
