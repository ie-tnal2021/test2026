# bench.py
import sys
import threading
import time

from sqlalchemy import create_engine, text


def main(url, n_threads, per_thread):
    """n_threads本のスレッドが、それぞれper_thread件をINSERTするのにかかる時間を計測して表示する。"""
    is_sqlite = url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    engine = create_engine(url, connect_args=connect_args)
    id_column = "INTEGER PRIMARY KEY" if is_sqlite else "SERIAL PRIMARY KEY"
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS t"))
        conn.execute(text(f"CREATE TABLE t (id {id_column}, v TEXT)"))

    errors = []

    def worker():
        """1本のスレッドとして、per_thread件をINSERTする。失敗した場合は、errorsに記録する。"""
        for _ in range(per_thread):
            try:
                with engine.begin() as conn:
                    conn.execute(text("INSERT INTO t (v) VALUES ('x')"))
            except Exception as e:
                errors.append(str(e)[:60])

    start = time.monotonic()
    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.monotonic() - start

    with engine.connect() as conn:
        saved = conn.execute(text("SELECT count(*) FROM t")).scalar()
    print(f"同時{n_threads}本 x {per_thread}件: {elapsed:.2f}秒 | 保存できた件数={saved} | 失敗={len(errors)}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))