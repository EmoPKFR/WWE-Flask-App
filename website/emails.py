from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # This means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from . import create_app, mail  # Import the create_app function

emails = Blueprint("emails", __name__)

@emails.route("/send_email_register")
def send_email_register():
    email = session.get("email")
    msg_title = "Confirm Your Account"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[email])
    
    data = {
        'app_name': "WWE Flask App",
        'title': msg_title,
    }

    msg.html = render_template("emails/register.html", data=data)

    try:
        mail.send(msg)
        flash("Check your Email to Create your account.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))


@emails.route("/confirm_register")
def confirm_register():
    email = session.get("email")
    username = session.get("username")
    password = session.get("password")
    card_number = session.get("card_number")
    expiry_date = session.get("expiry_date")
    cvv = session.get("cvv")
    
    if card_number is None:
        new_user = User(email=email, username=username, password=password)
    else:
        new_user = User(email=email, 
                        username=username, 
                        password=password, 
                        card_number=card_number,
                        expiry_date=expiry_date,
                        cvv=cvv)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True) 
    flash("Account created successfully!", category="success")
    return render_template("home.html", user=current_user)


@emails.route("/send_email_change_password", methods=["GET"])
def send_email_change_password():
    # Create the email message
    msg_title = "Change Password"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[current_user.email])
    
    new_password = session.get("new_password")
    
    data = {
        'app_name': "WWE Flask App",
        'title': msg_title,
        'new_password': new_password # Pass the new_password to the email template
    }

    msg.html = render_template("emails/change_password.html", data=data)

    try:
        mail.send(msg)
        flash("Check your Email to change your password.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_change_password")
def confirm_change_password():
    new_password = session.get("new_password")
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
    return render_template("home.html", user=current_user)
    

@emails.route("/send_email_delete_account")
def send_email_delete_account():
    # Create the email message
    msg_title = "Delete Account"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[current_user.email])
    
    data = {
        'app_name': "WWE Flask App",
        'title': msg_title,
    }

    msg.html = render_template("emails/delete_account.html", data=data)

    try:
        mail.send(msg)
        flash("Check your Email to delete your account.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_delete_account")
def confirm_delete_account():
    email = session.get("email")
    user = User.query.filter_by(email=email).first()
    db.session.delete(user)
    db.session.commit()
    flash("Account deleted successfully!", category="success")
    logout_user()
    return render_template("home.html", user=current_user)


@emails.route("/send_email_reset_password")
def send_email_reset_password():
    user_id = session.get("user_id")
    new_password = session.get("new_password")
    
    if user_id is not None:
        user = User.query.get(user_id)
    else:
        flash("User information not found in the session.", category="error")
        return redirect(url_for("views.home"))
    
    # Create the email message
    msg_title = "Reset Password"
    sender = "noreply@app.com"
    msg = Message(msg_title, sender=sender, recipients=[user.email])
       
    data = {
        'app_name': "WWE Flask App",
        'new_password': new_password # Pass the new_password to the email template
    }

    msg.html = render_template("emails/forgot_password.html", data=data)

    try:
        mail.send(msg)
        flash("Check your Email to change your password.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))


@emails.route("/send_order")
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

    data = {
        'app_name': "WWE Flask App",
        'title': msg_title,
        'products': products,
        'total_price': total_price,
        'formatted_total_amount_str': formatted_total_amount_str,
        'cart': cart
    }

    msg.html = render_template("emails/confirm_order.html", data=data)

    try:
        mail.send(msg)
        flash("Check your Email to Confirm your order.", category="success")
    except Exception as e:
        print(e)
        flash(f"The Email was not sent: {e}", category="error")

    return redirect(url_for("views.home"))

@emails.route("/confirm_order")
def confirm_order():
    products = session.get("products")
    total_price = session.get("total_price")
    shipping_address = session.get("shipping_address")
    
    new_order = Order(products=products , total_price=total_price, shipping_address=shipping_address,
                              email=current_user.email, username=current_user.username)
    
    db.session.add(new_order)
    db.session.commit()

    flash("The order has been sent successfully", category="success")
    
    
    return render_template("home.html", user=current_user)