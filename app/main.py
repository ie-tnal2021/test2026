from fastapi import FastAPI

app = FastAPI(title="WebAPI Course")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Dev Container is working!"}
