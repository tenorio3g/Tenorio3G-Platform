from flask import Blueprint, render_template

core = Blueprint("core", __name__)

@core.route("/")
def dashboard():
    return render_template("pages/dashboard.html")