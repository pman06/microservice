import secrets, hashlib, datetime
from datetime import timezone
from app.database import db
from app.models.email_verification import EmailVerificationToken
from app.models.user import User
from app.services.email_service import send_verification_email


MAX_RESENDS = 3

def generate_raw_token():
    return secrets.token_urlsafe(48)

def hash_token(raw):
    return hashlib.sha256(raw.encode()).hexdigest()

def create_email_verification_token(user, hours=24):
    raw_token = generate_raw_token()
    hashed = hash_token(raw_token)

    token = EmailVerificationToken(
        token_hash=hashed,
        user_id=user.id,
        expires_at= datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours)
    )

    db.session.add(token)
    db.session.commit()

    return raw_token

def verify_email_token(raw_token):
    hashed = hash_token(raw_token)
    token = db.session.query(EmailVerificationToken).filter_by(token_hash=hashed, used=False).first()

    if not token:
        return None, "invalid"
    
    if token.used:
        return None, "used"
    
    now = datetime.datetime.now(timezone.utc)
    expires_at = token.expires_at.replace(tzinfo=timezone.utc)
    if expires_at < now:
        success = resend_verification(token.user, token)
        if not success:
            return None, "resend_limit"
        return None, "resent"
    user = db.session.query(User).filter_by(id=token.user_id).first()

    token.used = True
    user.email_verified = True 
    db.session.commit()

    return user, "verified"

def resend_verification(user, old_token):
    
    if old_token.resent_count >= MAX_RESENDS:
        return False
    
    old_token.used = True
    old_token.resent_count += 1

    raw = create_email_verification_token(user)
    send_verification_email(user.email, raw)

    db.session.commit()
    return True