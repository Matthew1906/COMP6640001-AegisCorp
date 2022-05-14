from flask import Blueprint, jsonify, redirect, url_for
from flask_login import current_user
from ..models import Customer

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if current_user.is_authenticated:
        customers = Customer.query.all()
        result = [{'name':customer.user.name, "email":customer.user.email, 'image_url':customer.image_url} for customer in customers]
        return jsonify(result)
    else:
         return redirect(url_for('auth.login'))