from flask import Blueprint, jsonify, redirect, url_for
from flask_login import current_user
from ..models import User

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if current_user.is_authenticated:
        users = User.query.all()
        result = [{'name':user.name, "email":user.email} for user in users]
        return jsonify(result)
    else:
         return redirect(url_for('auth.login'))