from flask import Flask
from .database import db, migrate
from .routes.auth_routes import auth_bp
from .routes.admin_routes import admin_bp

def create_app(config_override=None):
    app = Flask(__name__)

    if config_override is not None:
        app.config.update(config_override)

    else:
        app.config.from_object('app.config.Config')

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app