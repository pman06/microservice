import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    return jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=3600)
        },
        current_app.config['JWT_SECRET'],
        algorithm="HS256"
    )