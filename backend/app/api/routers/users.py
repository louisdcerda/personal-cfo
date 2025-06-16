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

    # Serialize user data with datetime-safe output
    response_data = UserRead.model_validate(new_user).model_dump(mode="json")

    # Return JSON response with token as httponly cookie
    response = JSONResponse(content=response_data)
    response.set_cookie("access_token", token, httponly=True)
    return response


@router.post("/login")
def login(user: UserLogin, request: Request, db: Session = Depends(get_db)):
    # Fetch user by email
    db_user = db.query(User).filter(User.email == user.email).first()

    # Verify password
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create user session
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    session = create_user_session(db, db_user.id, ip, user_agent)

    # Serialize user using Pydantic model
    user_data = UserRead.model_validate(db_user).model_dump(mode="json")

    # Create response and set session token as secure, HttpOnly cookie
    response = JSONResponse(content={
        "message": "Login successful",
        "user": user_data
    })
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        secure=True,
        max_age=3600,  # 1 hour
        samesite="Lax"
    )
    return response


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user)


#checking to see if we should link bank for users who havent
@router.get("/should_link_bank")
def should_link_bank(current_user: User = Depends(get_current_user)):
    return {"should_link_bank": not current_user.has_linked_bank}


# after a user has linked their account update db
@router.post("update_link_bank")
def update_link_bank(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.has_linked_bank = True
    db.commit()
    return {"success": True}