from app.models.user import User
from app.database import db
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import generate_token

def register(email, password):
    # Check if user already exists by email
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return {'message': 'Error: Username already taken'}
    user = User(email=email, password=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return  {'message': 'User created successfully', 'id': user.id, 'email': user.email } 

def login(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return None
    return generate_token(user.id)