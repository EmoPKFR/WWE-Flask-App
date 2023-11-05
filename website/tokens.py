import secrets
import string
from flask_login import current_user
from . import db # This means from __init__.py import db

def generate_unique_token():
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    return token

from .models import ConfirmationToken
from datetime import datetime, timedelta

def store_token_in_database(token):
    expiration_time = datetime.now() + timedelta(hours=24)  # Token expires in 24 hours

    # Create a new record in your database
    new_token = ConfirmationToken(token=token,  user_id=current_user.id, expiration_time=expiration_time)
    db.session.add(new_token)
    db.session.commit()
    
def retrieve_order_data_from_token(token):
    # Retrieve the record from the database based on the token
    record = ConfirmationToken.query.filter_by(token=token).first()

    if record and record.expiration_time > datetime.now():
        return {
            'order_id': record.id
        }
    else:
        return None
        
def invalidate_token(token):
    record = ConfirmationToken.query.filter_by(token=token).first()
    if record:
        db.session.delete(record)
        db.session.commit()