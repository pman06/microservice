from flask import Flask
from .database import db, migrate
from .routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app