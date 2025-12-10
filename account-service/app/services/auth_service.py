from app.models.user import User
from app.database import db
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import generate_token

def register(email, password):
    user = User(email=email, password=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return user

def login(email, password):
    user = User.query.filter_by(email-email).first()
    if not user or not verify_password(password, user.password):
        return None
    return generate_token(user.id)