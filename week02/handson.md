# hands on
## ステップ1: curlで基本操作を試す
- curl -i https://jsonplaceholder.typicode.com/posts/1
    - ステータスコード: HTTP/2 200
    - Content-Typeヘッダ: content-type: application/json; charset=utf-8
```
HTTP/2 200 
date: Mon, 07 Sep 2026 05:44:45 GMT
content-type: application/json; charset=utf-8
content-length: 292
access-control-allow-credentials: true
cache-control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=AsU6Zb8kR58QnnK4hd4QT1uEqiPla2AtBdKVTrW6NKM%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1788576767"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=AsU6Zb8kR58QnnK4hd4QT1uEqiPla2AtBdKVTrW6NKM%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1788576767"
server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1788576772
age: 10306
accept-ranges: bytes
cf-cache-status: HIT
cf-ray: a3736743b925dd96-KIX
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

```
# POST
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "テスト投稿", "body": "これはテストです", "userId": 1}'
```

- post結果
    - ステータスコード: HTTP/2 201
    - Locationヘッダの有無: ある。https://jsonplaceholder.typicode.com/posts/101

```
HTTP/2 201 
date: Mon, 07 Sep 2026 05:46:10 GMT
content-type: application/json; charset=utf-8
content-length: 98
location: https://jsonplaceholder.typicode.com/posts/101
access-control-allow-credentials: true
access-control-expose-headers: Location
cache-control: no-cache
etag: W/"62-HBd6TFV3j9id85WDcMN6v7C8Jws"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=NGeW6kGSe%2F0lOh1czviLKAhgqXjmpqT2bLRsox75U%2FE%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1788759970"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=NGeW6kGSe%2F0lOh1czviLKAhgqXjmpqT2bLRsox75U%2FE%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1788759970"
server: cloudflare
vary: Origin, X-HTTP-Method-Override, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1788759976
cf-cache-status: DYNAMIC
cf-ray: a37369525813d3c5-KIX
alt-svc: h3=":443"; ma=86400

{
  "title": "テスト投稿",
  "body": "これはテストです",
  "userId": 1,
  "id": 101
}
```

---

## ステップ2: ブラウザDevToolsで観察する
