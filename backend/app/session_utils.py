import uuid
from datetime import datetime, timedelta
from app.models import UserSession

def create_user_session(db, user_id: int, ip_address: str, user_agent: str, duration_minutes: int = 60):
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)

    session = UserSession(
        user_id=user_id,
        session_token=token,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=expires_at,
        last_active_at=datetime.utcnow(),
    )

    db.add(session)
    db.commit()
    db.refresh(session)
    return session
