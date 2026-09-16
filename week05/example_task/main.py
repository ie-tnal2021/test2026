from fastapi import FastAPI, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db import get_db, engine
from database.models import Base
import database.models as db_models
from schemas import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI(title="タスク管理API", version="0.1.0")

Base.metadata.create_all(bind=engine)

@app.get("/api/v1/tasks", response_model=list[TaskResponse])
def list_tasks(done: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(db_models.Task)
    if done is not None:
        query = query.filter(db_models.Task.done == done)
    return query.all()

@app.post("/api/v1/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db_models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(db_models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.get(db_models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/v1/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.get(db_models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()