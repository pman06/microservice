import hashlib, secrets, datetime
from app.database import db
from app.models.refresh_token import RefreshToken
from flask import current_app

def generate_raw_refresh_token():
    return secrets.token_hex(64)

def hash_token(raw_token):
    return hashlib.sha256(raw_token.encode()).hexdigest()

def create_refresh_token_for_user(user, days=30):
    raw = generate_raw_refresh_token()
    h = hash_token(raw)
    now = datetime.datetime.now(datetime.timezone.utc)
    expires = now + datetime.timedelta(days=days)
    rt = RefreshToken(user_id=user.id, token_hash=h, issued_at=now, expires_at=expires)
    db.session.add(rt)
    db.session.commit()
    return raw

def revoke_refresh_token(raw_token):
    h = hash_token(raw_token)
    rt = RefreshToken.query.filter_by(token_hash=h, revoked=False).first()
    if not rt:
        return None
    rt.revoked = True
    db.session.commit()
    return True

def verify_and_rotate_refresh_token(raw_token, rotate=True, days=30):
    """
    Verify token exists not expired and not revoked
    If rotate=True: revoke old and insert new
    Returns (user, new_raw_token) or (None, None)
    """
    h = hash_token(raw_token)
    rt = RefreshToken.query.filter_by(token_hash=h, revoked=False).first()
    if not rt:
        return None, None
    now = datetime.datetime.now()

    if rt.expires_at < now:
        # mark as revoked/expired
        rt.revoked =True
        db.session.commit()
        return None, None
    
    user = rt.user

    if rotate:
        # revoke old
        rt.revoked =True
        new_raw = generate_raw_refresh_token()
        new_hash = hash_token(new_raw)
        expires = now + datetime.timedelta(days=days)
        new_rt = RefreshToken(user_id=user.id, token_hash=new_hash, issued_at=now, expires_at=expires)
        db.session.add(new_rt)
        db.session.commit()
        return (user, new_raw)
    else:
        return (user, None)