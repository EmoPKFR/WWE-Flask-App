from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from .models import User, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # This means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps

auth = Blueprint("auth", __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)  # Forbidden
        return fn(*args, **kwargs)
    return wrapper


@auth.route("/admin_dashboard")
def admin_dashboard():
    if current_user.is_authenticated and current_user.role == 'admin':
        return render_template('admin_dashboard.html', user=current_user)
    else:
        return render_template("auth/catch_all_routes.html")

@auth.route("/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)

    if user_to_delete:
        if user_to_delete.id != current_user.id:  # Avoid deleting the currently logged-in admin
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User deleted successfully.", category="success")
        else:
            flash("Cannot delete yourself.", category="error")
    else:
        flash("User not found.", category="error")

    return redirect(url_for("auth.database"))


def not_logged_in_required_with_message(message_category, message):
    def decorator(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated:
                flash(message, category=message_category)
                return redirect(url_for('auth.profile_page'))  # Redirect to a dashboard or any other logged-in route
            return view_func(*args, **kwargs)
        return decorated_view
    return decorator

@auth.route("/login", methods=["GET", "POST"])
@not_logged_in_required_with_message("warning", "You cannot go to Login Page when you are logged in.")
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                
                if user.role == "admin":
                    return redirect(url_for("auth.admin_dashboard"))
                else:
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
@not_logged_in_required_with_message("warning", "You cannot go to Register Page when you are logged in.")
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        card_number = request.form.get("card_number")
        # Remove spaces from the card number
        card_number = card_number.replace(" ", "")
        expiry_date = request.form.get("expiry_date")
        cvv = request.form.get("cvv")
        
        user = User.query.filter_by(email=email).first()
        username_check = User.query.filter_by(username=username).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 7:
            flash("Email must be at least 7 characters.", category="error")
        elif username_check:
            flash("Username already exists.", category="error")
        elif len(username) < 5:
            flash("Username must be at least 5 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters.", category="error")
        elif not card_number and not expiry_date and not cvv:
            session["email"] = email
            session["username"] = username
            session["password"] = generate_password_hash(password1, method="sha256")
            session["card_number"] = None
            session["expiry_date"] = None
            session["cvv"] = None
            return redirect(url_for("emails.send_email_register"))
        elif card_number and expiry_date and cvv:
            if len(card_number) != 16:
                flash("Card number must be exact 16 digits.", category="error")
            elif not cvv.isdigit() or len(cvv) != 3:
                flash("CVV must be exact 3 digits.", category="error")
            else:
                session["email"] = email
                session["username"] = username
                session["password"] = generate_password_hash(password1, method="sha256")
                session["card_number"] = generate_password_hash(card_number, method="sha256")
                session["expiry_date"] = expiry_date
                session["cvv"] = generate_password_hash(cvv, method="sha256")
                return redirect(url_for("emails.send_email_register"))
        else:
            flash("You have to fill Card Number, Expiry date and CVV or leave them Null.", category="error")
        
    return render_template("auth/register.html", user=current_user)

@auth.route("/profile_page")
@login_required
def profile_page():
    # Check if the user has a payment card
    user_has_payment_card = bool(current_user.card_number)

    return render_template("auth/profile_page.html", user=current_user, user_has_payment_card=user_has_payment_card)

@auth.route("/change_password", methods=["GET", "POST"])
@login_required
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
        elif new_password1 == new_password2 and len(new_password1) < 8:
            flash("Password must be at least 8 characters.", category="error")
        elif new_password1 != new_password2:
            flash("Passwords must match.", category="error")
        else:
            session["new_password"] = new_password1
            return redirect(url_for("emails.send_email_change_password"))

    return render_template("auth/change_password.html", user=current_user)

@auth.route("/forgot_password", methods=["GET", "POST"])
@not_logged_in_required_with_message("warning", "You cannot go to Forgot Password page when you are logged in.")
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        new_password1 = request.form.get("password1")
        new_password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()
        
        if new_password1 != new_password2:
            flash("Passwords don't match.", category="error")
        elif len(new_password1) < 8:
            flash("Password must be at least 8 characters.", category="error")
        elif user and check_password_hash(user.password, new_password1):
            flash("New password must be different than old password.", category="error")
        else:
            session["user_id"] = user.id
            session["email"] = email
            session["new_password"] = new_password1
            return redirect(url_for("emails.send_email_reset_password"))
        
    return render_template("auth/forgot_password.html", user=current_user)

@auth.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if current_user.email != email:
            flash("Wrong email or password.", category="error")
        elif not check_password_hash(current_user.password, password):
                flash("Wrong password or password.", category="error")
        else:
            session["email"] = email
            return redirect(url_for("emails.send_email_delete_account"))

    return render_template("auth/delete_account.html", user=current_user)

@auth.route("/add_payment_card", methods=["GET", "POST"])
@login_required
def add_payment_card():
    if request.method == "POST":
        card_number = request.form.get("card_number")
        # Remove spaces from the card number
        card_number = card_number.replace(" ", "")
        expiry_date = request.form.get("expiry_date")
        expiry_month = request.form.get("expiry_date")[:2]
        expiry_year = request.form.get("expiry_date")[-2:]
        cvv = request.form.get("cvv")
        
        if len(card_number) != 16:
            flash("Card number must be exact 16 digits.", category="error")
        elif not expiry_month.isdigit() or not expiry_year.isdigit() or int(expiry_month) > 12:
            flash("Expiry date must be filled in MM/YY format.", category="error")
        elif not cvv.isdigit() or len(cvv) != 3:
            flash("CVV must be exact 3 digits.", category="error")
        elif current_user.card_number is not None:
            if (current_user.card_number == int(card_number) or current_user.cvv == int(cvv) or
                (current_user.card_number == int(card_number) and current_user.expiry_date != expiry_date) or
                (current_user.cvv == int(cvv) and current_user.expiry_date != expiry_date)):
                flash("You cannot change your card with the same card or you have incorrect values", category="error")
            else:
                current_user.card_number = generate_password_hash(card_number, method="sha256")
                current_user.expiry_date = expiry_date
                current_user.cvv = generate_password_hash(cvv, method="sha256")
                db.session.commit()
                flash("Payment card changed successfully!", category="success")
                return redirect(url_for("views.home"))
        else:
            current_user.card_number = generate_password_hash(card_number, method="sha256")
            current_user.expiry_date = expiry_date
            current_user.cvv = generate_password_hash(cvv, method="sha256")
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
            session['admin_authenticated'] = True
            flash("Welcome to the Database", category="success")
            return redirect(url_for("auth.database"))
        else:
            flash("Wrong password", category="error")
        
    return render_template("auth/admin.html", user=current_user)

@auth.route("/database")
def database():
    if not session.get('admin_authenticated'):  # Check if the user is authenticated
        flash("Please log in as admin first", category="error")
        return redirect(url_for("auth.admin"))
    
    session['admin_authenticated'] = False
    users = User.query.all()
    orders = Order.query.all()
    print(users)  # Debug statement
    print(orders)  # Debug statement
    
    return render_template("auth/database.html", user=current_user, users=users, orders=orders)


@auth.route('/<path:path>')
def catch_all(path):
    # Here, you can generate or render example HTML or return a custom error page
    return render_template("auth/catch_all_routes.html")