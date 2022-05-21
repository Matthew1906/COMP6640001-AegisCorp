from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from ..models import TreatmentHeader
from ..utils import get_user_type, user_models

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if current_user.is_authenticated:
        user_type = get_user_type()
        user = user_models.get(user_type).query.filter_by(user_id=current_user.id)
        treatments = TreatmentHeader.query.all()
        return render_template('views.html', user=user, type=user_type, treatments=treatments)
    else:
         return redirect(url_for('auth.login'))