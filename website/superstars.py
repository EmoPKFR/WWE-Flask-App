from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # This means from __init__.py import db
from flask_login import current_user
from functools import wraps

superstars = Blueprint("superstars", __name__)


@superstars.route("/all_superstars")
def all_superstars():
    return render_template("superstars_info/all_superstars.html", user=current_user)

@superstars.route("/champions")
def champions():
    return render_template("superstars_info/champions.html", user=current_user)

@superstars.route("/roman_reigns")
def roman_reigns():
    return render_template("superstars_info/roman_reigns.html", user=current_user)

@superstars.route("/seth_rollins")
def seth_rollins():
    return render_template("superstars_info/seth_rollins.html", user=current_user)

@superstars.route("/rey_mysterio")
def rey_mysterio():
    return render_template("superstars_info/rey_mysterio.html", user=current_user)

@superstars.route("/carmelo_hayes")
def carmelo_hayes():
    return render_template("superstars_info/carmelo_hayes.html", user=current_user)

