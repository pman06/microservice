import jwt, datetime
from flask import current_app

def generate_token(user_id, role, minutes=15):

    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes)
    }
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET'],
        algorithm="HS256"
    )

def verify_token(token):
    try:
        payload = jwt.decode(token,current_app.config['JWT_SECRET'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None