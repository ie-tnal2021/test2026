# paperapi (論文メモAPI)

## エンドポイント一覧

| メソッド | パス | 認証 | 説明 |
| --- | --- | --- | --- |
| `POST` | `/api/v1/auth/register` | 不要 | ユーザー登録 |
| `POST` | `/api/v1/auth/login` | 不要 | ログイン（アクセストークン取得） |
| `GET` | `/api/v1/users/me` | 必要 (Bearer) | ログインユーザー情報取得 |
| `GET` | `/api/v1/papers` | 必要 (Bearer) | 論文一覧取得（クエリパラメータ: `done`, `q`） |
| `POST` | `/api/v1/papers` | 必要 (Bearer) | 論文作成 |
| `GET` | `/api/v1/papers/{paper_id}` | 必要 (Bearer) | 論文詳細取得 |
| `PATCH` | `/api/v1/papers/{paper_id}` | 必要 (Bearer) | 論文更新 |
| `DELETE` | `/api/v1/papers/{paper_id}` | 必要 (Bearer) | 論文削除 |

### POST リクエストのパラメータ詳細

#### 1. `POST /api/v1/auth/register` / `POST /api/v1/auth/login`
- **必須キー (Required)**:
  - `email` (`string` / EmailStr): メールアドレス
  - `password` (`string`): パスワード（最小8文字）
- **オプションキー (Optional)**: なし

#### 2. `POST /api/v1/papers`
- **必須キー (Required)**:
  - `title` (`string`): タイトル（1〜100文字）
- **オプションキー (Optional)**:
  - `published_date` (`integer` / `null`): 発行年（デフォルト: `null`、未来年指定不可）
  - `done` (`boolean`): 完了フラグ（デフォルト: `false`）
  - `memo` (`string` / `null`): メモ（デフォルト: `null`）

### PATCH リクエストのパラメータ詳細

#### 1. `PATCH /api/v1/papers/{paper_id}`
- **必須キー (Required)**: なし（部分更新のため、更新したいフィールドのみ指定）
- **オプションキー (Optional)**:
  - `title` (`string` / `null`): タイトル（1〜100文字）
  - `published_date` (`integer` / `null`): 発行年
  - `done` (`boolean` / `null`): 完了フラグ
  - `memo` (`string` / `null`): メモ
  - `created_at` (`string` / `null` / ISO 8601 DateTime): 作成日時

## セットアップ手順
- Dev Containerを開く
- 必要な環境変数（SECRET_KEY・DATABASE_URL等）を設定する
    - デモデータ挿入するseed.pyを使うなら、DEMO_EMAIL, DEMO_PASSWORDも設定する
- CI/CDを用意する
- uvicorn main:appで起動する
    - 例: `uvicorn main:app --host 0.0.0.0 --port 8000`
- ruffでLintチェックする: `ruff check .`
- pytestでテストを実行する: `pytest tests/ -v`
- 問題なければpush

## 本番URL
- https://test2026-m6iw.onrender.com/

## 本番DBを作成した日と、期限（作成の30日後）
- 作成日：2026年9月27日
- 予定期限：2026年10月27日

## DBの再構築手順
0 seed.pyの実行方法
    - .env に `DEMO_EMAIL`, `DEMO_PASSWORD`を設定。
    - `DATABASE_URL` を設定。
    - `python seed.py`

## バックアップの取得・復元のコマンド
- バックアップ取得
```
cd app

# .envのDEMO_EMAIL・DEMO_PASSWORDを、このシェルにも読み込む
set -a; source .env; set +a

# トークン取得
TOKEN=$(curl -s -X POST <本番URL>/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$DEMO_EMAIL\",\"password\":\"$DEMO_PASSWORD\"}" \
  | python3 -c 'import sys, json; print(json.load(sys.stdin)["access_token"])')

# バックアップ
cd ..  # リポジトリの直下へ戻る
mkdir backup
docker exec pg-local pg_dump -U app --no-owner --no-acl --clean --if-exists appdb > backup/appdb.sql

# 復元
docker run --rm -i postgres:16 psql "<External Database URL>" -v ON_ERROR_STOP=1 < backup/appdb.sql > /dev/null

# 動作確認例
docker run --rm postgres:16 psql "<External Database URL>" -c "select id, title, published_date, done from papers"
```
