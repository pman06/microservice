from app.models.user import User
from app.database import db
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import generate_token
from app.utils.refresh_token import create_refresh_token_for_user
from sqlalchemy import select

def register(email, password):
    # Check if user already exists by email
    # existing_email = User.query.filter_by(email=email).first()
    # OR
    # stmt = select(User).where(User.email == email)
    # existing_email = db.session.scalar(stmt).first()
    # OR
    existing_email = db.session.query(User).filter_by(email=email).first()

    if existing_email:
        # return errior if user doesn exist
        return {'message': 'Error: Username already taken'}
    # create new user
    new_user = User(email=email, password=hash_password(password))
    db.session.add(new_user)
    db.session.commit()

    # create user tokens
    access = generate_token(new_user.id, new_user.role)
    refresh_raw = create_refresh_token_for_user(new_user)
    return  {'message': 'User created successfully', 'user': new_user, 'access_token':access, 'refresh_token': refresh_raw } 

def login(email, password):
    user = db.session.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return None
    access = generate_token(user.id, user.role)
    refresh_raw = create_refresh_token_for_user(user)
    return {"user": user, "access_token": access, "refresh_token": refresh_raw}


