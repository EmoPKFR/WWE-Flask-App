from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(30))
    username = db.Column(db.String(20), unique=True)
    card_number = db.Column(db.Integer, nullable=True)
    expiry_date = db.Column(db.String(5), nullable=True)  # Store as "MM/YY"
    cvv = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    orders = db.relationship("Order")
    
    
    # Define the back-reference to the orders in the Order model
    orders = relationship("Order", back_populates="user")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.Column(db.String(50))
    total_price = db.Column(db.Float)
    shipping_address = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(20))
    email = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_order_user_id"))
    # Define a relationship to the User model
    user = relationship("User", back_populates="orders")
    
class ConfirmationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    used = db.Column(db.Boolean, default=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    
    def is_valid(self):
        return not self.used and self.expiration_time > datetime.now()
    
class TokenForRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True)
    user_email = db.Column(db.String(128))
    expiration_date = db.Column(db.DateTime)
    used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<TokenForRegister id={self.id}, user_email={self.user_email}, expiration_date={self.expiration_date}, used={self.used}>'
    