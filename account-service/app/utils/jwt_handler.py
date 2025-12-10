import jwt
import datetime
from flask import current_app

def generate_token(user_id, expires_in=3600):
    return jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        },
        current_app.config['JWT_SECRET'],
        algorithm="HS256"
    )