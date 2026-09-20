from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str

class PaperCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    published_date: Optional[int] = None
    done: bool = False
    memo: Optional[str] = None

    @field_validator("published_date")
    @classmethod
    def year_not_in_future(cls, v):
        current_year = date.today().year
        if v > current_year:
            raise ValueError(f"published_year must not be in the future (current year: {current_year})")
        return v

class PaperResponse(BaseModel):
    id: int
    title: str
    published_date: Optional[int]
    done: Optional[bool]
    memo: Optional[str]
    created_at: datetime

class PaperUpdate(BaseModel):
    title: Optional[str] = None
    published_date: Optional[int] = None
    done: Optional[bool] = None
    memo: Optional[str] = None
    created_at: Optional[datetime] = None
