from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from ... import crud, schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)
