# taskapi
## 脆弱性診断チェックリスト

### SQLi
- [OK] 文字列結合でSQLを組み立てている箇所がないか（grep "f\"SELECT" 等で検索）

### XSS（フロントエンドがある場合）
- [OK] innerHTML にユーザ入力を直接渡していないか
    - フロントエンドなし。

### CSRF
- [OK] Bearer Token方式で認証しているか（Cookieを使う場合はSameSite=Strictか）

### CORS
- [OK] allow_origins が "*" になっていないか

---

# app
## 脆弱性診断チェックリスト

### SQLi
- [OK] 文字列結合でSQLを組み立てている箇所がないか（grep "f\"SELECT" 等で検索）

### XSS（フロントエンドがある場合）
- [該当無し] innerHTML にユーザ入力を直接渡していないか

### CSRF
- [OK] Bearer Token方式で認証しているか（Cookieを使う場合はSameSite=Strictか）

### CORS
- [OK] allow_origins が "*" になっていないか
