import token, datetime
from datetime import timezone
from app.models.user import User
from app.models.email_verification import EmailVerificationToken
from app.database import db
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import generate_token
from app.utils.refresh_token import create_refresh_token_for_user
from app.utils.email_verification import create_email_verification_token, resend_verification
from app.services.email_service import send_verification_email

import logging
logger = logging.getLogger(__name__)

def register(email, password):
    # Check if user already exists by email
    # existing_email = User.query.filter_by(email=email).first()
    # OR
    # stmt = select(User).where(User.email == email)
    # existing_email = db.session.scalar(stmt).first()
    # OR
    existing_email = db.session.query(User).filter_by(email=email).first()

    if existing_email:
        # return errior if user doesn exist
        return {'message': 'Error: Username already taken'}
    # create new user
    new_user = User(email=email, password=hash_password(password))
    db.session.add(new_user)
    db.session.commit()

    # create user tokens
    access = generate_token(new_user.id, new_user.role)
    refresh_raw = create_refresh_token_for_user(new_user)

    # create email verification token
    token = create_email_verification_token(new_user)
    verify_link = send_verification_email(new_user.email, token)

    return  {'message': 'User created successfully', 'user': new_user, 'access_token':access, 'refresh_token': refresh_raw, 'verify_link': verify_link } 

def login(email, password):
    user = db.session.query(User).filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return None
    
    
    # Check if user is not verified before login then resend verification email if token expired
    if not user.email_verified:

        # if there is a token and it is expired resend else create new
        token = (db.session.query(EmailVerificationToken).filter_by(user_id=user.id, used=False)
                    .order_by(EmailVerificationToken.created.desc())
                    .first())
        if token:            
            now = datetime.datetime.now(timezone.utc)
            expires_at = token.expires_at.replace(tzinfo=timezone.utc)
            # If token.expires_at is naive, make it aware
            # if token.expires_at.tzinfo is None:
            #     # Assuming expires_at is stored as UTC in database
            #     expires_at = token.expires_at.replace(tzinfo=timezone.utc)
            # else:
            #     expires_at = token.expires_at

            if expires_at < now:
                success = resend_verification(user, token)
                if not success:
                    # Handle max resends reached
                    return {
                        "error": "Maximum resend attempts reached.",
                        "token": None,
                        "status_code": 403
                    }
        else:
            create_email_verification_token(user)
        return {"error": "Email not verified. Verification email resent",}
    
    # Create access tokens and refresh tokens
    access = generate_token(user.id, user.role)
    refresh_raw = create_refresh_token_for_user(user)

    return {"user": user, "access_token": access, "refresh_token": refresh_raw}


