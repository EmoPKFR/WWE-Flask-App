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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship("Order")
    
    
    # Define the back-reference to the orders in the Order model
    orders = relationship("Order", back_populates="user")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.Column(db.String(50))
    total_price = db.Column(db.Float)
    shipping_address = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(20))
    email = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_order_user_id"))
    # Define a relationship to the User model
    user = relationship("User", back_populates="orders")
    