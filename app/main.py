import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from database.db import get_db, engine
from database.models import Base
import database.models as db_models
from schemas import PaperCreate, PaperResponse, PaperUpdate, UserCreate, Token, UserResponse

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    print("Error: SECRET_KEY is not set in .env")
    exit(1)

ALGORITHM = "HS256"
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

app = FastAPI(title="論文メモ管理API", version="0.1.0")

Base.metadata.create_all(bind=engine)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(db_models.User).filter(db_models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/v1/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    db_user = db_models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post("/api/v1/auth/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token_expires = timedelta(minutes=30)
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode = {"sub": db_user.email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

@app.get("/api/v1/users/me", response_model=UserResponse)
def get_me(current_user: db_models.User = Depends(get_current_user)):
    return current_user

@app.get("/api/v1/papers", response_model=list[PaperResponse])
def list_papers(done: bool | None = None, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    query = db.query(db_models.Paper).filter(db_models.Paper.user_id == current_user.id)
    if done is not None:
        query = query.filter(db_models.Paper.done == done)
    return query.all()

@app.post("/api/v1/papers", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    existing_paper = db.query(db_models.Paper).filter(db_models.Paper.title == paper.title, db_models.Paper.user_id == current_user.id).first()
    if existing_paper:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Paper with this title already exists")
    db_paper = db_models.Paper(**paper.model_dump(), user_id=current_user.id)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@app.get("/api/v1/papers/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    paper = db.get(db_models.Paper, paper_id)
    if paper is None:
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
    if paper.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this paper")
    return paper


@app.patch("/api/v1/papers/{paper_id}", response_model=PaperResponse)
def update_paper(paper_id: int, paper_update: PaperUpdate, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    db_paper = db.get(db_models.Paper, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    if db_paper.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this paper")
    
    update_data = paper_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_paper, key, value)
    db.commit()
    db.refresh(db_paper)
    return db_paper


@app.delete("/api/v1/papers/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(paper_id: int, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    db_paper = db.get(db_models.Paper, paper_id)
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    if db_paper.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this paper")
    db.delete(db_paper)
    db.commit()
