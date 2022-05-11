from flask import Blueprint, jsonify
from ..models import User

views = Blueprint("views", __name__)

@views.route("/")
def home():
    users = User.query.all()
    result = [{'name':user.name, "email":user.email} for user in users]
    return jsonify(result)