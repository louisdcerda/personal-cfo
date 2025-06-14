from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models import UserSession
from app.core.config import settings
from fastapi import Depends, HTTPException, Request, status
from app.deps import get_db
from sqlalchemy.orm import Session


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing session token"
        )

    session = db.query(UserSession).filter(UserSession.session_token == token).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )
    
    session.last_active_at = datetime.utcnow()
    db.commit()

    return session.user
    