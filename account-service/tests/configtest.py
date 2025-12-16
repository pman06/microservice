import pytest
from app import create_app
from app.database import db
from app.models.user import User
from app.utils.password_hash import hash_password

@pytest_fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET": "test-secret"
        }
    )

    with app.context():
        db.create_all()
        yield app
        db.drop_all()

@pytest_fixture
def client(app):
    return app.test_client()

@pytyest_fixture
def user(app):
    u = User(
         email="user@test.com",
        password=hash_password("password"),
        role="user"
    )
    db.session.add(u)
    db.session.commit()
    return u

@pytest_fixture
def admin(app):
    u = user(
        email="admin@test.com",
        password=hash_password("password"),
        role="admin"
    )

    db.session.add(u)
    db.session.commit()
    return u