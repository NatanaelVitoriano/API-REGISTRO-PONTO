from sqlalchemy.orm import Session
from models import User, TimeLog
from schemas import UserCreate, TimeLogCreate
from auth.hashing import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_user_name(db: Session, user_name: str):
    return db.query(User).filter(User.user_name == user_name).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, user_name=user.user_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_time_log(db: Session, user_id: int):
    last_timelog = db.query(TimeLog).filter(TimeLog.user_id == user_id).order_by(TimeLog.timestamp.desc()).first()
    if last_timelog:
        db_log = TimeLog(user_id=user_id, action= ("check-in" if last_timelog.action == "check-out" else "check-out"))
    else:
        db_log = TimeLog(user_id=user_id, action= "check-in")
        
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_time_logs(db: Session, user_id: int):
    return db.query(TimeLog).filter(TimeLog.user_id == user_id).order_by(TimeLog.timestamp.desc()).all()
