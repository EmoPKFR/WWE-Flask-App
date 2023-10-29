from flask import Blueprint, render_template
from flask_login import login_required, current_user

shows = Blueprint("shows", __name__)

@shows.route("/shows")
def shows_page():
    return render_template("shows_info/shows.html", user=current_user)

@shows.route("/shows2")
def shows_page2():
    return render_template("shows_info/shows2.html", user=current_user)

@shows.route("/raw")
def raw():
    return render_template("shows_info/raw.html", user=current_user)

@shows.route("/smackdown")
def smackdown():
    return render_template("shows_info/smackdown.html", user=current_user)

@shows.route("/nxt")
def nxt():
    return render_template("shows_info/nxt.html", user=current_user)
