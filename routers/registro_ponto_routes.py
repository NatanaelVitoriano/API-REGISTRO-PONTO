from fastapi import APIRouter, Depends
from auth.auth import get_current_user
from crud import create_time_log, get_time_logs
from db import get_db
from schemas import TimeLog, TimeLogCreate, User
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/time_logs", tags=["Registro Ponto"], response_model=TimeLog)
def log_time(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Cria um registro de ponto para o usuário autenticado
    return create_time_log(db, user_id=current_user.id)

@router.get("/time_logs", tags=["Registro Ponto"], response_model=list[TimeLog])
def log_time(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Cria um registro de ponto para o usuário autenticado
    return get_time_logs(db, user_id=current_user.id)