import os
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from .models import User, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # This means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from . import mail  # Import the create_app function
from .tokens import (generate_unique_token, store_token_in_database as store_token_in_database1,
    retrieve_order_data_from_token, invalidate_token as invalidate_token1)
from .token_for_register import store_token_in_database as store_token_in_database2, verify_token,invalidate_token as invalidate_token2

emails = Blueprint("emails", __name__)

@emails.route("/send_email_register")
def send_email_register():
    """Sends an email to the user with a confirmation token."""

    # Get the user's email address
    email = session.get("email")

    # Generate a unique token and store it in the database
    confirmation_token2 = generate_unique_token()
    store_token_in_database2(confirmation_token2, email)

    # Create a message object
    msg = Message("Confirm Your Account", sender="noreply@app.com", recipients=[email])
    
    data = {
        'app_name': "WWE Flask App",
        'confirmation_token2': confirmation_token2
    }

    # Add the confirmation token to the message body
    msg.html = render_template("emails/register.html", confirmation_token2=confirmation_token2, data=data)

    # Try to send the email
    try:
        mail.send(msg)
        flash("Check your Email to Create your account.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))


@emails.route("/confirm_register/<token>")
def confirm_register(token):
    # Verify the token and check if it's valid and hasn't expired
    is_valid_token = verify_token(token)

    # If the token is valid, create a new user account
    if is_valid_token:
        # Create a new user object
        password = session.get("password")
        username = session.get("username")
        card_number = session.get("card_number")
        expiry_date = session.get("expiry_date")
        cvv = session.get("cvv")

        new_user = User(email=session.get("email"), password=password, username=username, card_number=card_number, expiry_date=expiry_date, cvv=cvv)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log in the user
        login_user(new_user, remember=True)
        flash("Account created successfully!", category="success")

        # Invalidate the token immediately after the user clicks on the link
        invalidate_token2(token)

        return render_template("redirect_from_email_links/register_success.html", user=current_user)
    else:
        flash("Invalid or expired confirmation link", category="error")
        return render_template("redirect_from_email_links/invalid_or_expired_link.html", user=current_user)


@emails.route("/send_email_change_password", methods=["GET"])
@login_required
def send_email_change_password():
    # Create the email message
    msg_title = "Change Password"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[current_user.email])
    
    confirmation_token1 = generate_unique_token()
    store_token_in_database1(confirmation_token1)
    
    new_password = session.get("new_password")
    
    data = {
        'app_name': "WWE Flask App",
        'new_password': new_password # Pass the new_password to the email template
    }

    msg.html = render_template("emails/change_password.html", data=data, change_password_token=confirmation_token1)

    try:
        mail.send(msg)
        flash("Check your Email to change your password.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_change_password/<change_password_token>")
def confirm_change_password(change_password_token):
    new_password = session.get("new_password")
    
    # Verify the token and check if it's valid and hasn't expired
    order_data = retrieve_order_data_from_token(change_password_token)
    
    if order_data is not None:
        # Invalidate the token to prevent further use
        invalidate_token1(change_password_token)
        
        if current_user.is_authenticated:
            current_user.password=generate_password_hash(new_password, method="sha256")  
        else:
            user_id = session.get("user_id")
            if user_id is not None:
                user = User.query.get(user_id)
                if user:
                    user.password = generate_password_hash(new_password, method="sha256")
                    login_user(user)
                else:
                    flash("User not found.", category="error")
            else:
                flash("User information not found in the session.", category="error")
        db.session.commit()
        flash("Password changed successfully!", category="success")
        return render_template("redirect_from_email_links/change_password_success.html", user=current_user)
    else:
        flash("Invalid or expired confirmation link", category="error")
        return render_template("redirect_from_email_links/invalid_or_expired_link.html", user=current_user)
    

@emails.route("/send_email_delete_account")
@login_required
def send_email_delete_account():
    # Create the email message
    msg_title = "Delete Account"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[current_user.email])
    
    confirmation_token1 = generate_unique_token()
    store_token_in_database1(confirmation_token1)
    
    data = {
        'app_name': "WWE Flask App"
    }

    msg.html = render_template("emails/delete_account.html", data=data, delete_account_token=confirmation_token1)

    try:
        mail.send(msg)
        flash("Check your Email to delete your account.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_delete_account/<delete_account_token>")
def confirm_delete_account(delete_account_token):
    # Verify the token and check if it's valid and hasn't expired
    order_data = retrieve_order_data_from_token(delete_account_token)
    
    if order_data is not None:
        # Invalidate the token to prevent further use
        invalidate_token1(delete_account_token)
        
        email = session.get("email")
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        flash("Account deleted successfully!", category="success")
        logout_user()
        return render_template("redirect_from_email_links/delete_account_success.html", user=current_user)
    else:
        flash("Invalid or expired confirmation link", category="error")
        return render_template("redirect_from_email_links/invalid_or_expired_link.html", user=current_user)


@emails.route("/send_email_reset_password")
def send_email_reset_password():
    email = session.get("email")
    new_password = session.get("new_password")

    user = User.query.filter_by(email=email).first()
    
    # Create the confirmation token
    reset_password_token = generate_unique_token()
    store_token_in_database2(reset_password_token, email)

    # Add the reset_password_token to the session object
    session["reset_password_token"] = reset_password_token

    # Create the email message
    msg_title = "Reset Password"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[email])

    data = {
        'app_name': "WWE Flask App",
        'reset_password_token': reset_password_token,
        'new_password': new_password
    }

    # Add the reset password token and the new password to the confirmation link

    msg.html = render_template("emails/forgot_password.html", reset_password_token=reset_password_token, data=data)

    try:
        mail.send(msg)
        flash("Check your Email to reset your password.", category="success")
    except Exception as e:
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_reset_password/<reset_password_token>")
def confirm_reset_password(reset_password_token):
    # Check if the reset_password_token is valid
    is_valid_token = verify_token(reset_password_token)
    
    if is_valid_token:
        email = session.get("email")
        new_password = session.get("new_password")

        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password, method="sha256")
        db.session.commit()
        login_user(user, remember=True)
        invalidate_token2(reset_password_token)
        
        flash("Password changed successfully!", category="success")
        return render_template("redirect_from_email_links/change_password_success.html", user=current_user)
    else:
        flash("Invalid or expired confirmation link", category="error")
        return render_template("redirect_from_email_links/invalid_or_expired_link.html", user=current_user)

@emails.route("/send_email_order")
@login_required
def send_email_order():
    products = session.get("products")
    total_price = session.get("total_price")
    total_product_price = session.get("total_product_price")
    cart = session.get("cart")
    msg_title = "Confirm Your Order"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[current_user.email])

    #Format the total amount to the second digit after the decimal point
    total_amount = round(total_product_price, 2)
    formatted_total_amount_str = "{:.2f}".format(total_amount)

    # Generate a unique token and store it in the database
    confirmation_token1 = generate_unique_token()
    store_token_in_database1(confirmation_token1)
    
    data = {
        'app_name': "WWE Flask App",
        'products': products,
        'total_price': total_price,
        'formatted_total_amount_str': formatted_total_amount_str,
        'cart': cart,
        'confirmation_token1': confirmation_token1
    }
    
    session["data"] = data

    msg.html = render_template("emails/confirm_order.html", data=data, confirm_order_token=confirmation_token1)

    try:
        mail.send(msg)
        flash("Check your Email to Confirm your order.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_order/<confirm_order_token>")
def confirm_order(confirm_order_token):
    # Verify the token and check if it's valid and hasn't expired
    order_data = retrieve_order_data_from_token(confirm_order_token)
    
    if order_data is not None:
        # Invalidate the token to prevent further use
        invalidate_token1(confirm_order_token)
        
        products = session.get("products")
        total_price = session.get("total_price")
        shipping_address = session.get("shipping_address")
        
        new_order = Order(products=products , total_price=total_price, shipping_address=shipping_address,
                                email=current_user.email, username=current_user.username)
        
        # Send an email to the admin with the order details
        send_email_to_admin_on_order_confirmation()
        
        db.session.add(new_order)
        db.session.commit()

        flash("The order has been sent successfully", category="success")
        
        
        return render_template("redirect_from_email_links/order_success.html", user=current_user)
    else:
        flash("Invalid or expired confirmation link", category="error")
        return render_template("redirect_from_email_links/invalid_or_expired_link.html", user=current_user)
    
    
def send_email_to_admin_on_order_confirmation():
    msg_title = "New order confirmation"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[os.environ.get("MAIL_USERNAME")])
    
    data = session.get("data")

    msg.html = render_template("emails/admin_confirm_order.html", user=current_user, data=data)

    try:
        mail.send(msg)
    except Exception as e:
        print(e)