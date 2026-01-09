def send_verification_email(email, token):
    verification_link = f"http://localhost:5000/verify/?token={token}"

    print("=====VERIFICATION EMAIL=====")
    print(f"To: {email}")
    print("Click: {verification_link}")
    print("============================")
    return verification_link

# import os

# PROVIDER = os.getenv("EMAIL_PROVIDER", "console")

# def send_email(to, subject, body):
#     if PROVIDER == "ses":
#         from app.services.providers.ses import send_via_ses
#         send_via_ses(to, subject, body)
#     elif PROVIDER == "sendgrid":
#         from app.services.providers.sendgrid import send_via_sendgrid
#         send_via_sendgrid(to, subject, body)
#     else:
#         # fallback for dev
#         print(f"EMAIL TO {to}\n{subject}\n{body}")