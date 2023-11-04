import secrets
import datetime
from . import db
from .models import TokenForRegister

def generate_unique_token():
    """Generates a unique token."""

    return secrets.token_urlsafe(32)

def store_token_in_database(token, user_email):
    """Stores a token in the database for a given user email."""

    # Create a new token record
    token_record = TokenForRegister(token=token, user_email=user_email, expiration_date=datetime.datetime.utcnow() + datetime.timedelta(seconds=15))

    # Add the token record to the database
    db.session.add(token_record)
    db.session.commit()

def verify_token(token):
    """Verifies a token and checks if it's valid and hasn't expired."""

    # Get the token record from the database
    token_record = TokenForRegister.query.filter_by(token=token).first()

    # If the token record is not found, or if the token has expired, or if the token has been used, return False
    if not token_record or token_record.expiration_date < datetime.datetime.utcnow() or token_record.used:
        return False

    # Otherwise, return True
    return True

def invalidate_token(token):
    """Invalidates a token by marking it as used."""

    # Get the token record from the database
    token_record = TokenForRegister.query.filter_by(token=token).first()

    # If the token record is found, mark it as used
    if token_record:
        token_record.used = True
        db.session.commit()
