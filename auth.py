from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import hashlib

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, password=hash_pw(password))
    db.add(user)
    db.commit()
    return {"msg": "User erstellt"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or user.password != hash_pw(password):
        return {"error": "Falsch"}

    return {"user_id": user.id}
