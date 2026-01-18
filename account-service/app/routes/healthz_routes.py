from flask import Blueprint
from app.controllers.health_controller import health_controller

health_bp = Blueprint('health', __name__)

health_bp.get("/")(health_controller)