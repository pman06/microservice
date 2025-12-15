from flask import Blueprint, jsonify
from app.utils.auth_decorators import admin_required, login_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.get("/admin/dashboard")
@admin_required
def admin_dashboard():
    return jsonify({"message": "Welcome admin"}), 200