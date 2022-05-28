from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..forms import InsuranceForm
from ..models import Customer, CustomerInsurance, InsuranceCompany, InsurancePolicy
from ..utils import customer_only

customer = Blueprint("customer", __name__)

@customer.route("/insurances")
@customer_only
def get_insurances():
    insurances = CustomerInsurance.query.filter_by(member_id=current_user.id)
    return render_template("customer.html", insurances=insurances, purpose='show')

@customer.route("/insurances/add", methods=['GET','POST'])
@customer_only
def add_insurance():
    form = InsuranceForm()
    form.company.choices = [(company.id, company.name) for company in InsuranceCompany.query.all()]
    if form.validate_on_submit():
        pass
    return render_template("customer.html", purpose='add', form=form)

@customer.route("/insurances/<int:company_id>/policies")
def get_policies(company_id:int):
    policies = InsurancePolicy.query.filter_by(company_id=company_id)
    return jsonify([{"id":policy.id, "name":policy.name} for policy in policies])
    