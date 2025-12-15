from app.models.user import User
from app.database import db
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import generate_token
from app.utils.refresh_token import create_refresh_token_for_user

def register(email, password):
    # Check if user already exists by email
    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        # return errior if user doesn exist
        return {'message': 'Error: Username already taken'}
    user = User(email=email, password=hash_password(password))
    db.session.add(user)
    db.session.commit()

    # create user tokens
    access = generate_token(user.id, user.role)
    refresh_raw = create_refresh_token_for_user(user)
    return  {'message': 'User created successfully', 'user': user, 'access_token':access, 'refresh_token': refresh_raw } 

def login(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return None
    access = generate_token(user.id, user.role)
    refresh_raw = create_refresh_token_for_user(user)
    return {"user": user, "access_token": access, "refresh_token": refresh_raw}


