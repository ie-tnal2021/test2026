# 自分のAPIのエンドポイント一覧をOpenAPIで設計する
## ステップ1: リソースを洗い出す
- ドメイン: 論文調査メモ管理
- リソース: 論文、著者、出典、読んだかどうか、メモ
- ユーザ: 自分（論文調査記録を残したい人）

## ステップ2: CRUD相当のエンドポイントを設計する
```
GET /api/v1/papers #一覧取得
GET /api/v1/papers/{id} #1件取得
POST /api/v1/papers # 作成
PUT /api/v1/papers/{id} #完全更新
```

## ステップ3: YAMLファイルとして書き出す
[openapi.yaml](./openai.yaml)
