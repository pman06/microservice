from functools import wraps
from flask import jsonify, request, g
from app.utils.jwt_handler import verify_token
from app.models.user import User
from ..database import db

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401

        token = auth.split(' ')[1]
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        user = db.session.get(User, payload['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 401
        
        g.current_user = user
        g.current_role = payload.get("role")

        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_check = login_required(lambda: None)
        result = auth_check()
        if result:
            return result
        
        if g.current_role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    return wrapper