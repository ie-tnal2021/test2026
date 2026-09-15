# 課題04-1: CRUDエンドポイントの実装

```
# GET/一覧
(base) oct2026:tnal% curl http://localhost:8000/api/v1/papers 
[]

# POST
(base) oct2026:tnal% curl -X POST http://localhost:8000/api/v1/papers -H "Content-Type: application/json" -d '{"title":"paper1"}'
{"id":1,"title":"paper1","published_date":null,"done":false,"memo":null,"created_at":"2026-09-15T01:28:05.369135"}

# GET/1件
(base) oct2026:tnal% curl http://localhost:8000/api/v1/papers/1
{"id":1,"title":"paper1","published_date":null,"done":false,"memo":null,"created_at":"2026-09-15T01:28:05.369135"}

# GET/1件、存在しないid
(base) oct2026:tnal% curl http://localhost:8000/api/v1/papers/100
{"detail":"Paper not found"}

# PATCH
(base) oct2026:tnal% curl -X PATCH http://localhost:8000/api/v1/papers/1 -H "Content-Type: application/json" -d '{"memo":"hoge"}'
{"id":1,"title":"paper1","published_date":null,"done":false,"memo":"hoge","created_at":"2026-09-15T01:28:05.369135"}

# DELETE
(base) oct2026:tnal% curl -X DELETE http://localhost:8000/api/v1/papers/1

# GET/1件
(base) oct2026:tnal% curl http://localhost:8000/api/v1/papers/1  
{"detail":"Paper not found"}

# GET/一覧
(base) oct2026:tnal% curl http://localhost:8000/api/v1/papers  
[]
```
