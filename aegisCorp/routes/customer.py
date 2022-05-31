from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .. import db
from ..forms import InsuranceForm
from ..models import Customer, CustomerInsurance, InsuranceCompany, InsurancePolicy
from ..utils import customer_only, user_models
import re as regex

customer = Blueprint("customer", __name__)

@customer.route("/insurances")
@customer_only
def get_insurances():
    user = user_models.get("Customer").query.filter_by(user_id=current_user.id).first()
    insurances = CustomerInsurance.query.filter_by(member_id=user.id)
    return render_template("customer.html", insurances=insurances, purpose='show')

@customer.route("/insurances/add", methods=['GET','POST'])
@customer_only
def add_insurance():
    form = InsuranceForm()
    if form.validate_on_submit():
        insurance_id = request.form.get("insurance_id").strip()
        if regex.search("^MEM_[0-9]{3}_POL_[0-9]{3}$", insurance_id):
            member_id, policy_id = [int(id) for id in insurance_id.split("_") if str(id).isdigit()]
            user = user_models.get("Customer").query.filter_by(user_id=current_user.id).first()
            if member_id != user.id:
                flash("Wrong Credentials!")
            else:
                find_insurance = CustomerInsurance.query.filter_by(member_id=member_id, policy_id = policy_id).first()
                if find_insurance:
                    flash("You are already registered for this insurance!")
                elif InsurancePolicy.query.filter_by(id=policy_id).first():
                    new_insurance = CustomerInsurance(
                        member_id=member_id, 
                        policy_id=policy_id,
                        expiration_date=datetime.now() + timedelta(days=1460)
                    )
                    db.session.add(new_insurance)
                    db.session.commit()
                    return redirect(url_for('customer.get_insurances'))
                else:
                    flash("Policy does not exist!")
        else:
            flash("Wrong Insurance Id!")
    return render_template("customer.html", purpose='add', form=form)
