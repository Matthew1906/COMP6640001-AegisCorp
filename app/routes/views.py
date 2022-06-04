from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import or_
from ..models import Customer, CustomerInsurance, Hospital, InsurancePolicy, TreatmentHeader, User
from ..utils import get_user_type, user_models

views = Blueprint("views", __name__)

@views.route("/")
def home():
    sort_filter = {'description':TreatmentHeader.description, 'hospital':Hospital.name, 'patient':User.name}
    if current_user.is_authenticated:
        user_type = get_user_type(current_user)
        user = user_models.get(user_type).query.filter_by(user_id=current_user.id).first()
        query = f'%{request.args.get("search") if request.args.get("search") not in [None, ""] else ""}%'
        treatments = TreatmentHeader.query.join(TreatmentHeader.customer)\
            .join(Customer.user).join(TreatmentHeader.hospital)\
                .filter(or_(Hospital.name.ilike(query), User.name.ilike(query),\
                    TreatmentHeader.description.ilike(query))).\
                        order_by(sort_filter.get(request.args.get('sort', 'description')))
        if user_type == 'Customer':
            treatments = treatments.filter(Customer.id==user.id)
        elif user_type == 'Hospital':
            treatments = treatments.filter(TreatmentHeader.hospital_id==user.hospital_id)
        elif user_type == 'Insurance':
            treatments = treatments.join(Customer.insurances).join(CustomerInsurance.policy).filter_by(company_id=user.company_id)
        return render_template('views.html', user=user, treatments=treatments, sort_by = request.args.get('sort'), search=request.args.get('search'))
    else:
         return redirect(url_for('auth.login'))