import datetime
from app.database import db

class EmailVerificationToken(db.Model):
    __tablename__ = "email_verification_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    # Add rate limiting for resending verification emails
    resent_count = db.Column(db.Integer, default=0)
    # # Add relationship to user
    # user = db.relationship('User', backref='verification_tokens')
