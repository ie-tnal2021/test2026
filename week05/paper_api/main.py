from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database.db import get_db, engine
from database.models import Base
import database.models as db_models
from datetime import datetime
from schemas import PaperCreate, PaperResponse, PaperUpdate

app = FastAPI(title="論文メモ管理API", version="0.1.0")

Base.metadata.create_all(bind = engine)

@app.get("/api/v1/papers", response_model=list[PaperResponse])
def list_papers(done: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(db_models.Paper)
    if done is not None:
        query = query.filter(db_models.Paper.done == done)
    return query.all()

@app.post("/api/v1/papers", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    db_paper = db_models.Paper(**paper.model_dump())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@app.get("/api/v1/papers/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.get(db_models.Paper, paper_id)
    if paper is None:
        #raise HTTPException(status_code=404, detail="Paper not found")
        raise HTTPException(
            status_code=404,
            detail={
                "type": "https://example.com/errors/not-found",
                "title": "Not Found",
                "status": 404,
                "detail": f"Paper {paper_id} not found",
                "instance": f"/api/v1/tasks/{paper_id}",
            },
        )
    return paper


@app.patch("/api/v1/papers/{paper_id}", response_model=PaperResponse)
def update_paper(paper_id: int, paper_update: PaperUpdate, db: Session = Depends(get_db)):
    db_paper = db.get(db_models.Paper, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    update_data = paper_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_paper, key, value)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@app.delete("/api/v1/papers/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    db_paper = db.get(db_models.Paper, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    db.delete(db_paper)
    db.commit()
