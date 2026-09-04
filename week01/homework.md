# week01/homework.md

## 課題01-1: GitHubリポジトリの作成確認

- リポジトリURL: https://github.com/<自分のGitHub ID>/<自分のリポジトリ名>

```
vscode ➜ /workspaces/test2026 (feature/week01-setup) $ git config --global user.name
Naruaki TOMA
vscode ➜ /workspaces/test2026 (feature/week01-setup) $ git config --global user.email
tnal@ie.u-ryukyu.ac.jp
```

## 課題01-2: 公開APIの調査

Open-Meteoを選択。

```
{"latitude":26.18629,"longitude":127.69737,"generationtime_ms":0.024080276489257812,"utc_offset_seconds":0timezone":"GMT","timezone_abbreviation":"GMT","elevation":0.0,"current_units":{"time":"iso8601","interval"seconds","temperature_2m":"°C"},"current":{"time":"2026-09-04T07:45","interval":900,"temperature_2m":29.1}
```

- 選んだAPI: Open-Meteo
- 実行したcurlコマンド: `curl "https://api.open-meteo.com/v1/forecast?latitude=26.2&longitude=127.6&current=temperature_2m"`
- 1行目のステータスコード: 
    - ステータスライン: HTTP/1.1 200 OK
    - 200になっている
- 気づいたこと
    - bodyのjsonが1行になっていて目視では確認しづらい。
- 疑問点
    - `Transfer-Encoding: chunked` とは何だろう？

---

## 01-3: この授業への一言
「評価する」に興味があります。「仕様通りに動く」以外にどのような観点で品質をどのように評価するのかが気になるため。

