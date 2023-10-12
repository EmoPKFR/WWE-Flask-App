from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")
    return render_template("auth/login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        card_number = request.form.get("card_number")
        expiry_date = request.form.get("expiry_date")
        cvv = request.form.get("cvv")
        
        user = User.query.filter_by(email=email).first()
        username_check = User.query.filter_by(username=username).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 3:
            flash("Email must be greater than 2 characters.", category="error")
        elif username_check:
            flash("Username already exists.", category="error")
        elif len(username) < 2:
            flash("Username must be greater than 5 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 3:
            flash("Password must be at least 6 characters.", category="error")
        elif not card_number and not expiry_date and not cvv:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) 
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
        elif card_number and expiry_date and cvv:
            if not card_number.isdigit() or len(card_number) != 10:
                flash("Card number must be exact 10 digits.", category="error")
            elif not cvv.isdigit() or len(cvv) != 3:
                flash("CVV must be exact 3 digits.", category="error")
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"), 
                                card_number=card_number, expiry_date=expiry_date,cvv=cvv)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True) 
                flash("Account created!", category="success")
                return redirect(url_for("views.home"))
        else:
            flash("You have to fill Card Number, Expiry Month, Expiry Year and CVV or leave them Null.", category="error")
        
    return render_template("auth/register.html", user=current_user)

@auth.route("/profile_page", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        if "change_password" in request.form:
            return redirect(url_for("auth.change_password"))
        if "delete_account" in request.form:
            return redirect(url_for("auth.delete_account"))
        if "add_payment_card" in request.form:
            return redirect(url_for("auth.add_payment_card"))
    
    # Check if the user has a payment card
    user_has_payment_card = bool(current_user.card_number)

    return render_template("auth/profile_page.html", user=current_user, user_has_payment_card=user_has_payment_card)

@auth.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password1 = request.form.get("new_password1")
        new_password2 = request.form.get("new_password2")
        
        if current_user.email != email:
            flash("Wrong email.", category="error")
        elif not check_password_hash(current_user.password, old_password):
                flash("Wrong password.", category="error")
        elif old_password == new_password1:
            flash("New password must be different than old password.", category="error")
        elif new_password1 == new_password2 and len(new_password1) < 3:
            flash("Passwords must be at least 3 characters.", category="error")
        elif new_password1 != new_password2:
            flash("Passwords must match.", category="error")
        else:
            current_user.password=generate_password_hash(new_password1, method="sha256")
            db.session.commit()
            flash("Password changed successfully!", category="success")
            return redirect(url_for("views.shop"))

    return render_template("auth/change_password.html", user=current_user)

@auth.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if current_user.email != email:
            flash("Wrong email or password.", category="error")
        elif not check_password_hash(current_user.password, password):
                flash("Wrong password or password.", category="error")
        else:
            user = User.query.filter_by(email=email).first()
            db.session.delete(user)
            db.session.commit()
            flash("Account deleted successfully!", category="success")
            logout_user()
            return redirect(url_for("auth.login"))

    return render_template("auth/delete_account.html", user=current_user)

@auth.route("/add_payment_card", methods=["GET", "POST"])
def add_payment_card():
    if request.method == "POST":
        card_number = request.form.get("card_number")
        expiry_date = request.form.get("expiry_date")
        expiry_month = request.form.get("expiry_date")[:2]
        expiry_year = request.form.get("expiry_date")[-2:]
        cvv = request.form.get("cvv")
        
        if not card_number.isdigit() or len(card_number) != 10:
            flash("Card number must be exact 10 digits.", category="error")
        elif not expiry_month.isdigit() or not expiry_year.isdigit() or int(expiry_month) > 12:
            flash("Expiry date must be filled in MM/YY format.", category="error")
        elif not cvv.isdigit() or len(cvv) != 3:
            flash("CVV must be exact 3 digits.", category="error")
        elif current_user.card_number is not None:
            # or (current_user.card_number == card_number and current_user.expiry_date == expiry_date) or (current_user.cvv == cvv and current_user.expiry_date == expiry_date)
            if (current_user.card_number == int(card_number) or current_user.cvv == int(cvv) or
                (current_user.card_number == int(card_number) and current_user.expiry_date != expiry_date) or
                (current_user.cvv == int(cvv) and current_user.expiry_date != expiry_date)):
                flash("You cannot change your card with the same card or you have incorrect values", category="error")
            else:
                current_user.card_number = card_number
                current_user.expiry_date = expiry_date
                current_user.cvv = cvv
                db.session.commit()
                flash("Payment card changed successfully!", category="success")
                return redirect(url_for("views.home"))
        else:
            current_user.card_number = card_number
            current_user.expiry_date = expiry_date
            current_user.cvv = cvv
            db.session.commit()
            flash("Payment card added successfully!", category="success")
            return redirect(url_for("views.home"))
    
    return render_template("auth/add_payment_card.html", user=current_user)

@auth.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        admin_password = "aaa"
        password = request.form.get("password")
        if password == admin_password:
            flash("Welcome to the Database", category="success")
            return redirect(url_for("auth.database"))
        else:
            flash("Wrong password", category="error")
        
    
    return render_template("auth/admin.html", user=current_user)

@auth.route("/database", methods=["GET", "POST"])
def database():
    if request.method == "POST":
        pass
    
    users = User.query.all()
    orders = Order.query.all()
    print(users)  # Debug statement
    print(orders)  # Debug statement
    
    return render_template("auth/database.html", user=current_user, users=users, orders=orders)

@auth.route('/<path:path>')
def catch_all(path):
    # Here, you can generate or render example HTML or return a custom error page
    return render_template("auth/catch_all_routes.html")