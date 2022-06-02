from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from .. import db
from ..models import Benefit, BenefitType, CheckUp, Customer, CustomerInsurance,\
    InsuranceCompany, InsurancePolicy, Medication, MedicationDetail, PolicyBenefit,\
        Procedure, ProcedureDetail, TreatmentClaim, TreatmentHeader, TreatmentDetail
from ..utils import get_treatment_cost, hospital_only, insurance_only
import pandas as pd
import json

insurance = Blueprint("insurance", __name__)

def get_best_policy_by_type(age, member_id, type):
    policy_query = select(InsuranceCompany.name.label("company"), \
        InsurancePolicy.name, (Benefit.price_limit*15000).label('coverage')).\
            join(CustomerInsurance.policy).join(InsurancePolicy.company).\
                join(InsurancePolicy.benefits).join(PolicyBenefit.benefit).\
                    join(Benefit.type).where(CustomerInsurance.member_id ==\
                        member_id, CustomerInsurance.expiration_date>=\
                            datetime.now(), age>=Benefit.min_age, age<=\
                                Benefit.max_age, BenefitType.name == type)
    policies = pd.read_sql(policy_query, db.session.bind)
    if len(policies)>0:
        chosen_policy = policies.loc[policies['coverage']==policies['coverage'].max()]
        return chosen_policy.iloc[0].to_dict()
    else:
        return {'coverage':0}

def get_detail_summary(id, policy, type):
    if type == 'checkup':
        details = select(CheckUp.price).join(TreatmentDetail.checkup).join(TreatmentDetail.doctor).where(TreatmentDetail.header_id == id)
    elif type == 'medication':
        details = select((Medication.price*15000*MedicationDetail.dosage).label('price')).join(TreatmentDetail.medication).join(MedicationDetail.medication).where(TreatmentDetail.header_id == id)
    else:
        details = select((Procedure.price*15000).label("price")).join(TreatmentDetail.procedure).join(ProcedureDetail.procedure).where(TreatmentDetail.header_id == id)
    df = pd.read_sql(details, db.session.bind)
    return {
        'policy':f"{policy.get('company')} - {policy.get('name')}" if policy.get('name') else None,
        'treatment_type':type.capitalize(),
        'total_price':int(df['price'].sum()),
        'insurance_coverage':policy.get('coverage'),
        'final_fee':int(df['price'].sum()) - policy.get('coverage') if int(df['price'].sum())>=policy.get('coverage') else 0
    }

def get_coverage_details(age, member_id, header_id):
    best_policies = [{'coverage':0}] + [
        get_best_policy_by_type(age, member_id, type) 
        for type in ['Medication', 'Procedure'] 
    ]
    detail_types = ['checkup', 'medication', 'procedure']
    return [get_detail_summary(header_id, policy, type) for policy, type in zip(best_policies, detail_types)]
    
@insurance.route("/claims/<int:treatment_id>", methods=['POST'])
@hospital_only
def claim_insurance(treatment_id:int):
    header = TreatmentHeader.query.filter_by(id=treatment_id).first()
    member = Customer.query.filter_by(id=header.customer_id).first()
    age = datetime.now().year - member.user.dob.year
    claim_report = get_coverage_details(age, member.id, header.id)
    new_claim = TreatmentClaim(
        member = member,
        treatment = header,
        claim_status = False,
        claim_report = json.dumps(claim_report)
    )
    db.session.add(new_claim)
    db.session.commit()
    return redirect(url_for('views.home'))
