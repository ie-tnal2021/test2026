# taskapi プロジェクトのコンテキスト

## 実行環境
- Dev Container内（Python 3.11、Debian bookworm）
- 仮想環境（venv）は使用していない。パッケージはグローバル環境にpip installでインストール済み
- fastapi・uvicorn・sqlalchemy・pydanticはインストール済み。pip list等で毎回確認する必要はない

## プロジェクト構成
- main.py: FastAPIアプリ本体、エンドポイント定義
- schemas.py: Pydanticモデル（リクエスト/レスポンスの型）
- database/models.py: SQLAlchemyのORMモデル
- database/db.py: DB接続・セッション管理

## 注意事項
- 自動テストは存在しない
- 新しい仮想環境の作成や、追加のパッケージインストールは行わない