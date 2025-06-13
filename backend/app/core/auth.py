from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models import UserSession

SECRET_KEY = "your-secret-key"  # move to .env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(status_code=401, details="Missing session token")

    session = db.query(UserSession).filter(UserSession.session_token == token).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, deatils="Session expired or invalid")
    
    session.last_active_at = datetime.utcnow()

    db.commit()

    return session.user
    