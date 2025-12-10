from flask import request, jsonify
from app.services.auth_service import register, login

def signup_controller():
    data = request.get_json()
    user = register(data['email'], data['password'])
    return jsonify({'id': user.id, 'email': user.email})

def login_controller():
    data = request.get_json()
    token = login(data['email'], data['password'])
    if not token:
        return jsonify({'error': 'Invalid credentials'})
    return jsonify({'token': token})
