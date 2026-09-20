## 認証コードレビューチェックリスト

- [ ] SECRET_KEY がハードコードされていないか（環境変数から読んでいるか）
- [ ] パスワードが平文やMD5/SHA-1等の弱いハッシュで保存されていないか（bcryptか）
- [ ] JWTのアルゴリズムが "none" になっていないか（署名検証が無効化されていないか）
- [ ] JWTの有効期限（exp）が設定されているか（有効期限がないと、トークンが漏洩した場合に攻撃者が無期限に使い続けられてしまう）
- [ ] トークン検証失敗時に 401 が返るか（500エラー等になっていないか）
- [ ] register 時の重複メールアドレスが 409 で拒否されるか
- [ ] login 失敗時のエラーメッセージが「emailが存在しない」と「パスワードが違う」を
      区別しすぎていないか（区別すると、登録済みメールアドレスの存在確認に悪用されうる）

### 指示に対する動作確認メモ
```
Implementing Authentication for taskapi: 
  I will research the existing database and schema structures in the `taskapi`
  project, then implement user authentication including registration, login, and
  JWT validation.

  ✓  ReadFile  database/models.py
  ✓  ReadFile  schemas.py
  ✓  ReadFile  database/db.py
╭──────────────────────────────────────────────────────────────────────────────────╮
│ ? Edit schemas.py: from pydantic import BaseModel... => from pydantic import B…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 3 hidden (Ctrl+O) ...                                                    │ │
│ │  3   from datetime import date, datetime                                     │ │
│ │  4                                                                           │ │
│ │ ════════════════════════════════════════════════════════════════════════════ │ │
│ │ 17       title: str                                                          │ │
│ │ 18       done: bool                                                          │ │
│ │ 19       due_date: Optional[date]                                            │ │
│ │ 20 -     created_at: datetime                                                │ │
│ │ 20 +     created_at: datetime                                                │ │
│ │ 21 +                                                                         │ │
│ │ 22 + class UserCreate(BaseModel):                                            │ │
│ │ 23 +     email: EmailStr                                                     │ │
│ │ 24 +     password: str = Field(..., min_length=8)                            │ │
│ │ 25 +                                                                         │ │
│ │ 26 + class Token(BaseModel):                                                 │ │
│ │ 27 +     access_token: str                                                   │ │
│ │ 28 +     token_type: str                                                     │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

環境が揃っている前提でコード変更をすぐさま提案してきた。
- schema.py
  - UserCreate()としてemail,passwordを追加。min_length=8は大きくしたいけど後で手動編集するだけで良さそう。
  - token()のaccess_token, token_typeがそれぞれただのstrで良いのか判断できないので、後で要確認。ひとまずそのまま承認。

```
? WriteFile  Writing to security.py                                              │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 14 hidden (Ctrl+O) ...                                                   │ │
│ │ 15     return password_hash.verify(plain_password, hashed_password)          │ │
│ │ 16                                                                           │ │
│ │ 17 def get_password_hash(password: str) -> str:                              │ │
│ │ 18     return password_hash.hash(password)                                   │ │
│ │ 19                                                                           │ │
│ │ 20 def create_access_token(data: dict, expires_delta: Optional[timedelta] =  │ │
│ │    None) -> str:                                                             │ │
│ │ 21     to_encode = data.copy()                                               │ │
│ │ 22     if expires_delta:                                                     │ │
│ │ 23         expire = datetime.now(timezone.utc) + expires_delta               │ │
│ │ 24     else:                                                                 │ │
│ │ 25         expire = datetime.now(timezone.utc) +                             │ │
│ │    timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)                            │ │
│ │ 26     to_encode.update({"exp": expire})                                     │ │
│ │ 27     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  │ │
│ │ 28     return encoded_jwt                                                    │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

セキュリティ周りの新規作成コード。
環境変数から読むこと、指定したHS256や30分制限もOK。
pwdlib.PasswordHashでハッシュ化して保存、verify。エンコードしたJWTで返すのも大丈夫そう。
=> 承認

```
 ? Edit main.py: from fastapi import FastAPI, H... => from fastapi import FastA…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 124 hidden (Ctrl+O) ...                                                  │ │
│ │  89           raise HTTPException(status_code=404, detail="Task not found")  │ │
│ │  90       update_data = task_update.model_dump(exclude_unset=True)           │ │
│ │  95       return db_task                                                     │ │
│ │  96                                                                          │ │
│ │  97   @app.delete("/api/v1/tasks/{task_id}",                                 │ │
│ │       status_code=status.HTTP_204_NO_CONTENT)                                │ │
│ │  50 - def delete_task(task_id: int, db: Session = Depends(get_db)):          │ │
│ │  51 -     db_task = db.get(db_models.Task, task_id)                          │ │
│ │ ════════════════════════════════════════════════════════════════════════════ │ │
│ │  98 + def delete_task(task_id: int, db: Session = Depends(get_db),           │ │
│ │     current_user: db_models.User = Depends(get_current_user)):               │ │
│ │  99 +     db_task = db.query(db_models.Task).filter(db_models.Task.id ==     │ │
│ │     task_id, db_models.Task.user_id == current_user.id).first()              │ │
│ │ 100       if db_task is None:                                                │ │
│ │ 101           raise HTTPException(status_code=404, detail="Task not found")  │ │
│ │ 102       db.delete(db_task)                                                 │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

main.pyの編集。
get_current_user()でauthenticationがまとまっている。
/api/v1/auth/register, loginが追加されている。
create_task, get_task, update_task, delete_taskにはget_current_userが依存性として設定されている。
=> 承認

```
I have implemented the requested authentication features for the taskapi project.

  Summary of Changes:
   1. schemas.py: Added UserCreate (email, password) and Token (access_token,
      token_type) models.
   2. security.py: Created this new file to handle password hashing using pwdlib
      (Argon2), password verification, and JWT creation with python-jose.
   3. main.py:
       * Implemented get_current_user dependency for JWT validation.
       * Implemented /api/v1/auth/register (POST) to register users.
       * Implemented /api/v1/auth/login (POST) to issue JWT tokens.
       * Updated existing /api/v1/tasks/* endpoints to require authentication via
         get_current_user and ensure they only operate on tasks belonging to the
         authenticated user.

  All endpoints are now protected and follow the requested authentication logic.
```

完了報告が出力されて終了。

---

### 追加実装（/api/v1/users/me）
```
/api/v1/users/me (GET) を実装してください。
- users/me: get_current_user に依存し、ログイン中のユーザー自身の情報を返す。
   トークンがない・不正な場合は401を返す。
```

```
? Edit schemas.py: class UserCreate(BaseModel):... => class UserCreate(BaseMod…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 3 hidden (Ctrl+O) ...                                                    │ │
│ │ 26 + class UserResponse(BaseModel):                                          │ │
│ │ 27 +     id: int                                                             │ │
│ │ 28 +     email: EmailStr                                                     │ │
│ │ 29 +                                                                         │ │
│ │ 30   class Token(BaseModel):                                                 │ │
│ │ 31       access_token: str                                                   │ │
│ │ 32       token_type: str                                                     │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

schemas.pyにレスポンス用クラスを作成。
passwordを含まない点含めて良いので承認。

```
 ? Edit main.py: from fastapi import FastAPI, H... => from fastapi import FastA…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 11 hidden (Ctrl+O) ...                                                   │ │
│ │ ════════════════════════════════════════════════════════════════════════════ │ │
│ │ 58       access_token = create_access_token(data={"sub": db_user.email})     │ │
│ │ 59       return {"access_token": access_token, "token_type": "bearer"}       │ │
│ │ 60                                                                           │ │
│ │ 61 + @app.get("/api/v1/users/me", response_model=UserResponse)               │ │
│ │ 62 + def get_me(current_user: db_models.User = Depends(get_current_user)):   │ │
│ │ 63 +     return current_user                                                 │ │
│ │ 64 +                                                                         │ │
│ │ 65   @app.get("/api/v1/tasks", response_model=list[TaskResponse])            │ │
│ │ 66  def list_tasks(done: bool | None = None, q: str | None = None, db:       │ │
│ │     Session = Depends(get_db), current_user: db_models.User =                │ │
│ │     Depends(get_current_user)):                                              │ │
│ │ 67       query = db.query(db_models.Task).filter(db_models.Task.user_id ==   │ │
│ │      current_user.id)                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

Depends(get_current_user)で返すエンドポイントの実装。
承認。

```
 I have implemented the /api/v1/users/me endpoint.

  Summary of Changes:
   1. schemas.py: Added UserResponse model containing id and email to safely return
      user profile information without sensitive data like passwords.
   2. main.py: Added the /api/v1/users/me (GET) endpoint. It uses the
      get_current_user dependency to retrieve the authenticated user and
      automatically handles unauthorized access (401) if the token is missing or
      invalid.
```

完了報告。
テーブル周りは問題ない？　ひとまずそのまま動作確認してみる。


---

### 演習/レビュー
認証コードレビューチェックリスト

- [OK] SECRET_KEY がハードコードされていないか（環境変数から読んでいるか）
    - `SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-for-development")` は、os.environの戻り値が辞書型であり、環境変数がない場合のデフォルト値が第2引数となっているだけ。
- [OK] パスワードが平文やMD5/SHA-1等の弱いハッシュで保存されていないか（Argon2等のパスワード用アルゴリズムか）
    - helpで `Currently, the hasher is Argon2 with default parameters.` を確認。
- [OK] JWTのアルゴリズムが "none" になっていないか（署名検証が無効化されていないか）
    - security.pyで `jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)`, `ALGORITHM = "HS256"` と指定されていることを確認。
- [OK] JWTの有効期限（exp）が設定されているか（有効期限がないと、トークンが漏洩した場合に攻撃者が無期限に使い続けられてしまう）
    - security.pyで以下のように設定されていることを確認。
        - `ACCESS_TOKEN_EXPIRE_MINUTES = 30`
        - `expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)`
        - `to_encode.update({"exp": expire})`
- [OK] トークン検証失敗時に 401 が返るか（500エラー等になっていないか）
    - main.pyのget_current_user()で以下の設定を確認。
        - `credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")`
- [OK] register 時の重複メールアドレスが 409 で拒否されるか
    - filter後に重複チェックし、重複時に `raise HTTPException(status_code=409, detail="Email already registered")` していることを確認。
- [OK] login 失敗時のエラーメッセージが「emailが存在しない」と「パスワードが違う」を
      区別しすぎていないか（区別すると、登録済みメールアドレスの存在確認に悪用されうる）
    - `detail="Incorrect email or password"` として、どちらか判断できないようになっていることを確認。