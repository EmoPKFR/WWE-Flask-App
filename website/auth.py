from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
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
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 3:
            flash("Email must be greater than 2 characters.", category="error")
        elif len(username) < 2:
            flash("Username must be greater than 2 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 3:
            flash("Password must be at least 3 characters.", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) 
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
        
    return render_template("auth/register.html", user=current_user)

@auth.route("/profile_page", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        if "change_password" in request.form:
            return redirect(url_for("auth.change_password"))
        if "delete_account" in request.form:
            return redirect(url_for("auth.delete_account"))
    
    return render_template("auth/profile_page.html", user=current_user)

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


    

# @auth.route('/<path:path>')
# def catch_all(path):
#     # Here, you can generate or render example HTML or return a custom error page
#     return render_template("auth/catch_all_routes.html")