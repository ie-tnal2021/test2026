# Week02

## 課題02-1: 選んだ公開APIの分析レポート
- 演習で選んだ（または新たに選ぶ）公開API: [Wheather Forcast API](https://open-meteo.com/en/docs)
- 使われているHTTPメソッド
    - GET
    - 明示的な記載はないが、全操作がURL取得のみ・書き込み操作が存在しないことから、暗黙的にGETのみが使われていると判断できる
- 代表的なステータスコード
    - 400（ドキュメントより）
    - 200（curlで確認）
        - curl -i "https://api.open-meteo.com/v1/forecast?latitude=52.52&lon
gitude=13.41&hourly=temperature_2m"
- レスポンス形式
    - latitude, longitudeのように経度緯度情報がある。timezoneも指定されているらしい。
```
HTTP/1.1 200 OK
Date: Mon, 07 Sep 2026 07:40:27 GMT
Content-Type: application/json; charset=utf-8
Transfer-Encoding: chunked
Connection: keep-alive

{"latitude":52.52,"longitude":13.419998,"generationtime_ms":0.06580352783203125,"utc_offset_seconds":0,"timezone":"GMT","timezone_abbreviation":"GMT","elevation":38.0,"hourly_units":{"time":"iso8601","temperatu
（略）
```

## 課題02-2: 自分が作るAPIのドメイン企画書


