from flask import request, jsonify
from app.services.auth_service import register, login

def signup_controller():
    data = request.get_json()
    response = register(data['email'], data['password'])
    print(response)
    if response['message'] == 'Error: Username already taken':
        return jsonify({'error': 'Email already registered'}), 409
    return jsonify({'id': response['id'], 'email': response['email']})

def login_controller():
    data = request.get_json()
    token = login(data['email'], data['password'])
    if not token:
        return jsonify({'error': 'Invalid credentials'})
    return jsonify({'token': token})
