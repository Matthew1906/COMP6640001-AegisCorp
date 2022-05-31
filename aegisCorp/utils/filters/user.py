from datetime import datetime
from ...models import Customer, HospitalStaff, InsuranceStaff

user_models={'Customer':Customer, 'Hospital':HospitalStaff, 'Insurance':InsuranceStaff}

def get_user_type(current_user):
    hospital_staff = HospitalStaff.query.filter_by(user_id = current_user.id).first()
    insurance_staff = InsuranceStaff.query.filter_by(user_id = current_user.id).first()
    customer = Customer.query.filter_by(user_id = current_user.id).first()
    if hospital_staff:
        return 'Hospital'
    elif insurance_staff:
        return 'Insurance'
    else:
        return "Customer"

def format_date(date):
    return date.strftime("%d/%m/%Y")

def format_age(date):
    return datetime.now().year - date.year

def format_marital_status(status):
    return "Married" if status else "Single"

def format_gender(status):
    return "♂" if status else '♀'
