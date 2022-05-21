from flask import abort
from flask_login import current_user
from functools import wraps
from ..models import Customer, HospitalStaff, InsuranceStaff

user_models={'Customer':Customer, 'Hospital':HospitalStaff, 'Insurance':InsuranceStaff}

def get_user_type():
    hospital_staff = HospitalStaff.query.filter_by(user_id = current_user.id).first()
    insurance_staff = InsuranceStaff.query.filter_by(user_id = current_user.id).first()
    customer = Customer.query.filter_by(user_id = current_user.id).first()
    if hospital_staff:
        return 'Hospital'
    elif insurance_staff:
        return 'Insurance'
    else:
        return "Customer"

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