from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..deps import get_db
from ..utils import hash_password, verify_password
from app.models import User, UserSession
from app.core.auth import create_access_token, create_user_session, get_current_user
from app.schemas import UserCreate, UserRead, UserLogin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserRead)
def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already signed up with this email"
        )

    # Hash password and create user
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token = create_access_token(data={"sub": new_user.email})

    # Return response with cookie and serialized data
    response_data = UserRead.model_validate(new_user)

    from fastapi.responses import Response
    response = Response(
        content=response_data.model_dump_json(),
        media_type="application/json"
    )
    response.set_cookie("access_token", token, httponly=True)
    return response


@router.post("/login")
def login(user: UserLogin, request: Request, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    session = create_user_session(db, db_user.id, ip, user_agent)

    response = JSONResponse(content={
        "message": "Login successful",
        "user": UserRead.model_validate(db_user).dict(),  
    })
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        secure=True,
        max_age=3600,
        samesite="Lax"
    )
    return response


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user) 
