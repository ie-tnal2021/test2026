# week10/homework.md

## 課題10-1: デプロイの安定化とREADME整備
[app/README.md](../app/README.md)

## 【オプション】課題10-2: SQLiteとPostgreSQLの、同時書き込みを比べる
```
(bench-venv) (base) oct2026:tnal% python3 bench.py sqlite:///./bench.db 1 300
同時1本 x 300件: 0.12秒 | 保存できた件数=300 | 失敗=0
(bench-venv) (base) oct2026:tnal% python3 bench.py sqlite:///./bench.db 20 30 
同時20本 x 30件: 0.36秒 | 保存できた件数=600 | 失敗=0
(bench-venv) (base) oct2026:tnal% python3 bench.py postgresql+psycopg2://postgres:pw@localhost:15432/bench 1 300
同時1本 x 300件: 0.22秒 | 保存できた件数=300 | 失敗=0
(bench-venv) (base) oct2026:tnal% python3 bench.py postgresql+psycopg2://postgres:pw@localhost:15432/bench 20 30 
同時20本 x 30件: 0.18秒 | 保存できた件数=600 | 失敗=0
```

- 「1本で順番に書き込む場合」: SQLite 0.12秒 < PostgreSQL 0.22秒
- 「同時に20本で書き込む場合」: PostgreSQL 0.18秒 < SQLite 秒。

SQLiteは書き込み中はDB全体をロックし書き込みを1つずつ順番に処理するため遅いが、同時1本ならば早い。同時20本ではPostgreSQLが早い。
