from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    done: bool = False
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    due_date: Optional[date] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    due_date: Optional[date]
    created_at: datetime