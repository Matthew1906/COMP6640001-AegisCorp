from flask import Blueprint, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/customers/register", methods=['GET','POST'])
def register():
    pass

@auth.route("/<user_type>/login", methods=['GET', 'POST'])
def login(user_type:str):
    # user_type = customers, hospitals, insurances
    pass

@login_required
@auth.route("/<user_type>/logout", methods=['GET', 'POST'])
def logout(user_type:str):
    # user_type = customers, hospitals, insurances
    logout_user()
    return redirect(url_for('views.home'))