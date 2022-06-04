from flask import abort
from flask_login import current_user
from functools import wraps
from ..models import Customer, HospitalStaff, InsuranceStaff

# Decorators
def customer_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and Customer.query.filter_by(user_id =current_user.id).first():
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function

def hospital_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and HospitalStaff.query.filter_by(user_id =current_user.id).first():
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function

def insurance_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and InsuranceStaff.query.filter_by(user_id =current_user.id).first():
            return func(*args, **kwargs)
        return abort(403)
    return decorated_function