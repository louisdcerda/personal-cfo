from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from ... import crud, schemas
from ..utils import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@orouter.post("/signup", response_model=schemes.UserRead)
def user_signup(user:schemas.UserCreate, db: Session = Depends(get_db)):
    # creating a new user if not present based on email

    # check if user is in db already 
    if user in db.UserRead:
        return "Error user already signed up with email"


    existing_user = db.query(User).filter(User.email == user.email).first() # getting the first user with the email

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detial="User already signed up with this email"
        )

    hashed_password = hash_password(user.password)


    # create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user