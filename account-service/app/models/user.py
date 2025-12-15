from app.database import db
import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    refresh_tokens = db.relationship('RefreshToken',  backref='user', lazy='dynamic', cascade='all, delete-orphan')
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    # adding roles to Db
    role = db.Column(db.String(20), nullable=False, default='user', server_default='user')

    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_email(self):
        return self.email