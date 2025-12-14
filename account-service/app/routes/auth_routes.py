from flask import Blueprint
from app.controllers.auth_controller import signup_controller, login_controller, refresh_controller, logout_controller

auth_bp = Blueprint('auth', __name__)

auth_bp.post("/signup")(signup_controller)
auth_bp.post("/login")(login_controller)
auth_bp.post("/refresh")(refresh_controller)
auth_bp.post("/logout")(logout_controller)