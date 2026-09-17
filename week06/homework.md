# 課題06-1: 指示の曖昧さによる出力の比較

## 曖昧な指示
### 指示内容
重複しないようにして

### 挙動ログと実行状況
- 1回目: 指示入力
```
> 重複しないようにして                                                             

  Investigating Duplication Requirement: 
  Understand what the user wants to avoid duplicating by analyzing the context
  of homework.md and clarifying the requirement.

  ✓  ReadFolder  . → Found 10 item(s).
╭──────────────────────────────────────────────────────────────────────────────────╮
│ Answer Questions                                                                 │
│                                                                                  │
│ Could you please clarify what you would like to ensure is not duplicated? For    │
│ example, are you referring to data in the database, API endpoints, or something  │
│ in your homework document?                                                       │
│                                                                                  │
│ > What should not be duplicated?                                                 │
```

- 2回目: 良く分からないと言われたのでもう少し詳しく入力してみる
```
> 論文タイトル重複しないようにして

│ ✓  Ask User                                                                  │
│                                                                              │
│ User answered:                                                               │
│   Clarification → 論文タイトル                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
  Preventing Duplicate Paper Titles: 
  Implement a check to ensure research paper titles are unique in the database.

  ✓  ReadFile  database/models.py
  ✓  ReadFile  main.py
╭──────────────────────────────────────────────────────────────────────────────────╮
│ ? Edit database/models.py:     title = Column(String(100)... =>     title = Co…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ 14   class Paper(Base):                                                      │ │
│ │ 15       __tablename__ = "papers"                                            │ │
│ │ 16       id = Column(Integer, primary_key=True, autoincrement=True)          │ │
│ │ 17 -     title = Column(String(100), nullable=False)                         │ │
│ │ 17 +     title = Column(String(100), unique=True, nullable=False)            │ │
│ │ 18       published_date = Column(Integer, default=None, nullable=True)       │ │
│ │ 19       done = Column(Boolean, default=False, nullable=True)                │ │
│ │ 20       memo = Column(String(1024), default=None, nullable=True)            │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

models.pyで、titleに unique=True を追加。大丈夫そうなので許可。

```
│ ? Edit main.py: @app.post("/api/v1/papers", re... => @app.post("/api/v1/papers…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ 19                                                                           │ │
│ │ 20   @app.post("/api/v1/papers", response_model=PaperResponse,               │ │
│ │      status_code=status.HTTP_201_CREATED)                                    │ │
│ │ 21   def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):    │ │
│ │ 22 +     existing_paper =                                                    │ │
│ │    db.query(db_models.Paper).filter(db_models.Paper.title ==                 │ │
│ │    paper.title).first()                                                      │ │
│ │ 23 +     if existing_paper:                                                  │ │
│ │ 24 +         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,    │ │
│ │    detail="Paper with this title already exists")                            │ │
│ │ 25       db_paper = db_models.Paper(**paper.model_dump())                    │ │
│ │ 26       db.add(db_paper)                                                    │ │
│ │ 27       db.commit()                                                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

main.pyにおける @app.post への変更。filter(title).first()で検索し、存在するなら400返すように提案。ひとまず了承。

```
? WriteFile  Writing to test_duplication.py                                      │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 16 hidden (Ctrl+O) ...                                                   │ │
│ │ 17     response1 = client.post("/api/v1/papers", json=paper_data)            │ │
│ │ 18     assert response1.status_code == 201                                   │ │
│ │ 19                                                                           │ │
│ │ 20     # Second creation (should fail)                                       │ │
│ │ 21     response2 = client.post("/api/v1/papers", json=paper_data)            │ │
│ │ 22     assert response2.status_code == 400                                   │ │
│ │ 23     assert response2.json()["detail"] == "Paper with this title already   │ │
│ │    exists"                                                                   │ │
│ │ 24                                                                           │ │
│ │ 25 if __name__ == "__main__":                                                │ │
│ │ 26     # Run test                                                            │ │
│ │ 27     try:                                                                  │ │
│ │ 28         test_create_duplicate_paper()                                     │ │
│ │ 29         print("Test passed: Duplicate title prevention is working.")      │ │
│ │ 30     except Exception as e:                                                │ │
│ │ 31         print(f"Test failed: {e}")                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

動作チェック用のテストファイルの作成を提案している。これも承認。

```
 ? Shell  python3 /workspaces/test2026/app/test_duplication.py                    │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ python3 /workspaces/test2026/app/test_duplication.py                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

テストコードの実行許可も承認。

```
 ? Shell  pip list                                                                │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ pip list                                                                     │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

ライブラリ足りない（確かにやってない）ので確認了承。

```
? Edit  test_duplication.py: from fastapi.testclient import... => import reques… │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 50 hidden (Ctrl+O) ...                                                   │ │
│ │ 29 +         print(f"Test failed: Expected 400, got {response2.status_code}, │ │
│ │    {response2.json()}")                                                      │ │
│ │ 30 +         sys.exit(1)                                                     │ │
│ │ 31 +                                                                         │ │
│ │ 32 +     print("Test passed: Duplicate title prevention is working.")        │ │
│ │ 33                                                                           │ │
│ │ 25 - if __name__ == "__main__":                                              │ │
│ │ 26 -     # Run test                                                          │ │
│ │ 27 -     try:                                                                │ │
│ │ 28 -         test_create_duplicate_paper()                                   │ │
│ │ 29 -         print("Test passed: Duplicate title prevention is working.")    │ │
│ │ 30 -     except Exception as e:                                              │ │
│ │ 31 -         print(f"Test failed: {e}")                                      │ │
│ │ 34 + finally:                                                                │ │
│ │ 35 +     process.terminate()                                                 │ │
│ │ 36 +     process.wait()                                                      │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

確認した上でテストに使えそうなパッケージがなかったのと、GEMINI.mdによる指示「新しい仮想環境の作成や、追加のパッケージインストールは行わない」に基づいて、追加インストール無しで動作するテストに変更するらしい。問題ないので承認。

```
? Shell  python3 /workspaces/test2026/app/test_duplication.py                    │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ python3 /workspaces/test2026/app/test_duplication.py                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

改めてテスト実行要求してきたので承認。

```
 ✓  Shell python3 /workspaces/test2026/app/test_duplication.py                │
│                                                                              │
│ ... 2 hidden (Ctrl+O) ...                                                    │
│ INFO:     Application startup complete.                                      │
│ INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)    │
│ INFO:     127.0.0.1:37712 - "POST /api/v1/papers HTTP/1.1" 201 Created       │
│ INFO:     127.0.0.1:37722 - "POST /api/v1/papers HTTP/1.1" 400 Bad Request   │
│ Test passed: Duplicate title prevention is working.                          │
│ INFO:     Shutting down                                                      │
│ INFO:     Waiting for application shutdown.                                  │
│ INFO:     Application shutdown complete.                                     │
│ INFO:     Finished server process [147784]                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────╮
│ ? Shell  rm /workspaces/test2026/app/test_duplication.py                         │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ rm /workspaces/test2026/app/test_duplication.py                              │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?   
```

テストが想定通りに終わったのを確認できたら、ファイルが不要なので削除を申請。問題ないので承認。

```
Task Completion: Conclude the task and provide a summary of the changes.


✦ I have implemented the requirement to prevent duplicate research paper titles.

  Here is a summary of the changes:

   1. Database Model Update: Added unique=True to the title column in
      database/models.py within the Paper class to enforce uniqueness at the
      database level.
   2. API Logic Update: Updated the create_paper endpoint in main.py to check if a
      paper with the same title already exists before attempting to create it. If a
      duplicate is found, the API now returns a 400 Bad Request error.

  I verified these changes by creating and running a test script that attempts to
  create a paper with a duplicate title, which confirmed the expected behavior (the
  second request correctly returns a 400 status code).
```

タスク終了報告で終了。

### 動作確認
完全一致タイトルをPOSTできるか確認してみたところ、適切にエラー(400)返すようになっている。これで動作確認終了とし、コミットする。

```
(base) oct2026:tnal% curl -X POST http://localhost:8000/api/v1/papers \
  -H "Content-Type: application/json" \
  -d '{"title": "論文10"}'
{"id":5,"title":"論文10","published_date":null,"done":false,"memo":null,"created_at":"2026-09-17T07:00:26"}
(base) oct2026:tnal% curl -X POST http://localhost:8000/api/v1/papers \
  -H "Content-Type: application/json" \
  -d '{"title": "論文10"}'
{"detail":"Paper with this title already exists"}
```

### diff

---

## 具体的な指示
### 指示内容
POST /api/v1/papers で論文メモを新規追加する際、titleが完全一致するデータが存在する場合は追加せず、409 Conflict を返すようにしてください。レスポンスで json を返し、detail には "same title exist" を含めてください。

### gemini挙動

```
? Edit main.py: @app.post("/api/v1/papers", re... => @app.post("/api/v1/papers…  │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ 19                                                                           │ │
│ │ 20   @app.post("/api/v1/papers", response_model=PaperResponse,               │ │
│ │      status_code=status.HTTP_201_CREATED)                                    │ │
│ │ 21   def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):    │ │
│ │ 22 +     existing_paper =                                                    │ │
│ │    db.query(db_models.Paper).filter(db_models.Paper.title ==                 │ │
│ │    paper.title).first()                                                      │ │
│ │ 23 +     if existing_paper:                                                  │ │
│ │ 24 +         raise HTTPException(                                            │ │
│ │ 25 +             status_code=status.HTTP_409_CONFLICT,                       │ │
│ │ 26 +             detail="same title exist"                                   │ │
│ │ 27 +         )                                                               │ │
│ │ 28       db_paper = db_models.Paper(**paper.model_dump())                    │ │
│ │ 29       db.add(db_paper)                                                    │ │
│ │ 30       db.commit()                                                         │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

すぐさま具体的な変更を提案してきた。filter(title).first()になっており、409を返す点まで指示通り。承認。

```
 ? WriteFile  Writing to test_main.py                                             │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 12 hidden (Ctrl+O) ...                                                   │ │
│ │ 13 def test_create_paper_duplicate_title():                                  │ │
│ │ 14     # 1. Create a paper                                                   │ │
│ │ 15     paper_data = {"title": "Test Paper", "memo": "Test memo"}             │ │
│ │ 16     response = client.post("/api/v1/papers", json=paper_data)             │ │
│ │ 17     assert response.status_code == 201                                    │ │
│ │ 18                                                                           │ │
│ │ 19     # 2. Try to create the same paper again                               │ │
│ │ 20     response = client.post("/api/v1/papers", json=paper_data)             │ │
│ │ 21     assert response.status_code == 409                                    │ │
│ │ 22     assert response.json() == {"detail": "same title exist"}              │ │
│ │ 23                                                                           │ │
│ │ 24 def test_create_paper_different_title():                                  │ │
│ │ 25     # 3. Create a different paper                                         │ │
│ │ 26     paper_data = {"title": "Different Paper", "memo": "Test memo"}        │ │
│ │ 27     response = client.post("/api/v1/papers", json=paper_data)             │ │
│ │ 28     assert response.status_code == 201                                    │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

続けてテスト作成を提案している。この挙動はアバウト指示と同様。テストを指定していなかった場合には動作確認するように学習していると想像。テスト作成自体は問題ないが、pytest想定してるのがネック。ひとまず承認して、アバウト指示と同様のルートを辿るか確認することに。

```
? Shell  pytest test_main.py                                                     │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ pytest test_main.py                                                          │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

pytest実行許可を求めてきたので承認。

```
? Shell  pip list | grep httpx                                                   │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ pip list | grep httpx                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

モジュール不足になったので環境確認するところも同じ。

```
? Shell  pip list                                                                │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ pip list                                                                     │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

これも承認。

```
? WriteFile  Writing to verify_duplicate_check.py                                │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ ... 13 hidden (Ctrl+O) ...                                                   │ │
│ │ 14     paper_data = {"title": "Test Paper", "memo": "Test memo"}             │ │
│ │ 15     response = requests.post(base_url, json=paper_data)                   │ │
│ │ 16     print(f"First request status: {response.status_code}")                │ │
│ │ 17     assert response.status_code == 201                                    │ │
│ │ 18                                                                           │ │
│ │ 19     # 2. Try to create the same paper again                               │ │
│ │ 20     response = requests.post(base_url, json=paper_data)                   │ │
│ │ 21     print(f"Second request status: {response.status_code}")               │ │
│ │ 22     print(f"Second request response: {response.json()}")                  │ │
│ │ 23     assert response.status_code == 409                                    │ │
│ │ 24     assert response.json() == {"detail": "same title exist"}              │ │
│ │ 25     print("Test passed!")                                                 │ │
│ │ 26 finally:                                                                  │ │
│ │ 27     # Clean up: stop the server                                           │ │
│ │ 28     os.kill(process.pid, signal.SIGTERM)                                  │ │
│ │ 29     process.wait()                                                        │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Apply this change?                                                               │
```

pytestなしのテストコードを提案で、ここまで同じルートを辿っている。承認。

```
? Shell  python3 verify_duplicate_check.py                                       │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ python3 verify_duplicate_check.py                                            │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

実行承認。

```
? Shell  rm verify_duplicate_check.py test_main.py                               │
│ ╭──────────────────────────────────────────────────────────────────────────────╮ │
│ │ rm verify_duplicate_check.py test_main.py                                    │ │
│ ╰──────────────────────────────────────────────────────────────────────────────╯ │
│ Allow execution of [Shell]?                                                      │
```

テスト後にファイル削除するのも同じ。承認。

```
✦ I have implemented the duplicate title check in POST /api/v1/papers.

  Changes Made:
   - Modified /workspaces/test2026/app/main.py: Updated the create_paper function to
     query the database for an existing paper with the same title before adding a
     new one. If found, it now raises an HTTPException with status code 409 Conflict
     and {"detail": "same title exist"}.

  Verification:
   - Created a reproduction script (verify_duplicate_check.py) that launches the
     application using uvicorn and uses the requests library to verify the new
     behavior.
   - The script confirmed that the first request succeeds (201) and the second
     request with the same title results in a 409 Conflict with the correct error
     message.
   - Temporary test files have been removed.
```

完了報告で終了。

### 動作確認
ちゃんと重複時に指定した文言を含むdetailをjsonで返し、409になっていることも確認。問題ないのでコミットすることに。

```
(base) oct2026:tnal% curl -i -X POST http://localhost:8000/api/v1/papers \
  -H "Content-Type: application/json" \
  -d '{"title": "論文10"}'
HTTP/1.1 409 Conflict
date: Thu, 17 Sep 2026 07:17:33 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"same title exist"}
```

---

## diff
### diff結果
```
vscode ➜ /workspaces/test2026 (experiment/specific-prompt) $ git diff experiment/vag
ue-prompt..experiment/specific-prompt -- app/
diff --git a/app/database/models.py b/app/database/models.py
index 42a987a..afc5edb 100644
--- a/app/database/models.py
+++ b/app/database/models.py
@@ -14,7 +14,7 @@ class User(Base):
 class Paper(Base):
     __tablename__ = "papers"
     id = Column(Integer, primary_key=True, autoincrement=True)
-    title = Column(String(100), unique=True, nullable=False)
+    title = Column(String(100), nullable=False)
     published_date = Column(Integer, default=None, nullable=True)
     done = Column(Boolean, default=False, nullable=True)
     memo = Column(String(1024), default=None, nullable=True)
diff --git a/app/main.py b/app/main.py
index 57db573..924c4be 100644
--- a/app/main.py
+++ b/app/main.py
@@ -21,7 +21,10 @@ def list_papers(done: bool | None = None, db: Session = Depends(get_db)):
 def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
     existing_paper = db.query(db_models.Paper).filter(db_models.Paper.title == paper.title).first()
     if existing_paper:
-        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Paper with this title already exists")
+        raise HTTPException(
+            status_code=status.HTTP_409_CONFLICT,
+            detail="same title exist"
+        )
     db_paper = db_models.Paper(**paper.model_dump())
     db.add(db_paper)
     db.commit()
```

### 対応
動作自体は詳細指示の方が適切であり、指示通り409や "same title exit" を返している。一方、title制約についてはアバウト指示において model.py で unique=True を設定しており、モデル制約として導入するシンプル設計に見える。よって今回はシンプル設計を採用し、409を返すように修正したものを提出版とする。

```
git checkout experiment/vague-prompt

# ここで main.py を編集し、status.HTTP_409_CONFLICT を返すように修正。
# 改めて動作確認。

git add week06/homework.md
git commit -m "Add comparison notes"
git push -u origin experiment/vague-prompt

# GitHub上でPRを作成し、mainにマージ

# ローカルリポジトリ後片付け
git checkout main
git pull origin main
git branch -d experiment/vague-prompt
```

## 備考
テストコード作りがちなので指示に含めた方が良さそう。
