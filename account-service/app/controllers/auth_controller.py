from flask import request, jsonify
from app.utils.jwt_handler import generate_token
from app.services.auth_service import register, login
from app.utils.refresh_token import verify_and_rotate_refresh_token, revoke_refresh_token

def signup_controller():
    data = request.get_json()
    response = register(data['email'], data['password'])
    print(response)
    if response['message'] == 'Error: Username already taken':
        return jsonify({'error': 'Email already registered'}), 409
    
    return jsonify({'message': response['message'], 
                    'email': response['user'].get_email(), 
                    'access_token': response['access_token'],
                    'refresh_token': response['refresh_token']}), 201

def login_controller():
    data = request.get_json()
    token = login(data['email'], data['password'])
    if not token:
        return jsonify({'error': 'Invalid credentials'})
    return jsonify({'user': token['user'].get_email(), 'access_token': token['access_token'], 'refresh_token': token['refresh_token']})


def refresh_controller():
    data = request.get_json(silent=True) or {}
    raw = data.get('refresh_token') or request.cookies.get('refresh_token')
    if not raw:
        return jsonify({'error': 'no refresh token provided'}), 400
    
    user, new_raw = verify_and_rotate_refresh_token(raw)

    if not user:
        return jsonify({'error': 'Invalid or expired refresh token'}), 401
    
    access = generate_token(user.id, user.role)
    resp ={'access_token': access}
    if new_raw:
        resp['refresh_token'] = new_raw
    return jsonify(resp)

def logout_controller():
    data = request.get_json(silent=True) or {}
    raw = data.get('refresh_token') or request.cookies.get('refresh_token')
    if not raw:
        return jsonify({'error': ' no refresh token provided'}), 400
    
    ok = revoke_refresh_token(raw)
    if ok :
        return jsonify({'status': 'ok'}), 200
    
    return jsonify({'error': 'token not found'}), 400