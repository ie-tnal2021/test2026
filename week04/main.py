from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from schemas import PaperCreate, PaperResponse, PaperUpdate

app = FastAPI(title="タスク管理API", version="0.1.0")

papers_db: list[dict] = []  # データベースの代わりに、メモリ上のリストにタスクを保存する（第5回でDBに置き換える）
next_id = 1

@app.get("/api/v1/papers", response_model=list[PaperResponse])
def list_tasks(done: bool | None = None):
    if done is None:
        return papers_db
    return [t for t in papers_db if t["done"] == done]

@app.post("/api/v1/papers", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(paper: PaperCreate):
    global next_id
    new_paper = {
        "id": next_id, "title": paper.title,
        "published_date": paper.published_date,
        "done": paper.done,
        "memo": paper.memo,
        "created_at": datetime.now(),
    }
    papers_db.append(new_paper)
    next_id += 1
    return new_paper

@app.get("/api/v1/papers/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int):
    paper = next((p for p in papers_db if p["id"] == paper_id), None)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@app.patch("/api/v1/papers/{paper_id}", response_model=PaperResponse)
def update_paper(paper_id: int, paper_update: PaperUpdate):
    paper = next((p for p in papers_db if p["id"] == paper_id), None)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    update_data = paper_update.model_dump(exclude_unset=True)
    paper.update(update_data)
    return paper

@app.delete("/api/v1/papers/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(paper_id: int):
    paper = next((p for p in papers_db if p["id"] == paper_id), None)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    papers_db.remove(paper)
