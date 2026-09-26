# 課題09-1: app/へのテスト・Lint・CIの適用
## ruff, pytestの結果
```
(.venv) vscode ➜ /workspaces/test2026/app (main) $ ruff check .
All checks passed!
(.venv) vscode ➜ /workspaces/test2026/app (main) $ pytest tests/ -v
============================================ test session starts =============================================
platform linux -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0 -- /workspaces/test2026/.venv/bin/python
cachedir: .pytest_cache
rootdir: /workspaces/test2026/app
configfile: pytest.ini
plugins: cov-7.1.0, anyio-4.15.1
collected 9 items                                                                                            

tests/test_papers.py::test_list_papers_empty PASSED                                                    [ 11%]
tests/test_papers.py::test_create_and_get_paper PASSED                                                 [ 22%]
tests/test_papers.py::test_create_paper_validation_error PASSED                                        [ 33%]
tests/test_papers.py::test_search_returns_only_matching_titles PASSED                                  [ 44%]
tests/test_papers.py::test_search_can_be_combined_with_done PASSED                                     [ 55%]
tests/test_papers.py::test_register_duplicate_email_returns_409 PASSED                                 [ 66%]
tests/test_papers.py::test_login_with_wrong_password_returns_401 PASSED                                [ 77%]
tests/test_papers.py::test_papers_without_token_returns_401 PASSED                                     [ 88%]
tests/test_papers.py::test_search_is_not_vulnerable_to_sql_injection PASSED                            [100%]

============================================== warnings summary ==============================================
../.venv/lib/python3.11/site-packages/starlette/testclient.py:53
  /workspaces/test2026/.venv/lib/python3.11/site-packages/starlette/testclient.py:53: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = Callable[[], AbstractContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================== 9 passed, 1 warning in 1.00s ========================================
```

CI (app) も成功。

---

## 課題09-2: カバレッジの計測と、テスト追加の判断

1. 最初に計測したときのTOTALのCover（%）
- 79%

2. テストを追加した場合は、追加したテストと、追加した理由（どのMissingの行に対応するか）


3. 最終的な実行結果（pytest --cov=. --cov-report=term-missingの出力）

4. 最終結果でもMissingに残っている行があれば、行（または行の範囲）ごとに、テストを追加しなかった理由

### Missing 詳細チェック
- database/db.py:9-13
    - DBを用意するコード。テストコードではテスト用DBに差し替えているため、テスト不要。
- main.py:18-19
    - SECRET_KEYが存在しない場合のコード。既にこれ自体がテストになっているが、今回は実装パス？
- main.py:38-40
    - 38-39: email指定がない場合のコード。=> test_token_without_sub_returns_401()
- main.py: 43
- main.py: 73
- main.py: 88
- main.py: 100
- main.py: 111
- main.py: 117-128
- main.py: 133-139
- schemas.py: 26-29
