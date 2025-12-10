from app.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name