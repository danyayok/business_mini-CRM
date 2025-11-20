from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.auth import RegisterReq, LoginReq, RegisterResponse, LoginResponse
from app.services.auth import AuthService

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterReq, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(data.email, data.password, data.name, data.organization_name)

@router.post("/login", response_model=LoginResponse)
def login(data: LoginReq, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data.email, data.password)