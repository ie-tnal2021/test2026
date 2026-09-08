# preview.py（今回限りの確認用スクリプト）
import yaml
from fastapi import FastAPI

app = FastAPI()
with open("openapi.yaml") as f:
    spec = yaml.safe_load(f)

app.openapi = lambda: spec  # FastAPI自身のスキーマ生成をやめ、読み込んだYAMLをそのまま使わせる