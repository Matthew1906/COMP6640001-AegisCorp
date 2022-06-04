from ...models import TreatmentClaim, TreatmentHeader
from .utils import currency, format_id
import json

def format_insurance_id(insurance):
    return f"MEM_{format_id(insurance.member_id)}_POL_{format_id(insurance.policy_id)}"

def get_insurance_benefits(insurance):
    return [f"Coverage for {benefit.benefit.type.name.capitalize()} \
        with maximum fee of {currency(benefit.benefit.price_limit*15000)} - \
        applicable for age {benefit.benefit.min_age}-{benefit.benefit.max_age}" 
        for benefit in insurance.policy.benefits
    ]
    
def get_insurance_company(insurance):
    return insurance.policy.company.name

def get_insurance_policy(insurance):
    return insurance.policy.name

def get_claim_status(treatment_id:int):
    header = TreatmentHeader.query.filter_by(id=treatment_id).first()
    claim = TreatmentClaim.query.filter_by(treatment_id=treatment_id, member_id=header.customer_id).first()
    if claim and claim.claim_status:
        return 1
    elif claim and not claim.claim_status:
        return 0
    else:
        return -1

def jsonify(report:str):
    return json.loads(report)

def format_price(price):
    return currency(price)

def get_coverage_status(report):
    if report.get('insurance_coverage')>=report.get('total_price'):
        return 'Completely covered'
    elif report.get('policy') !=None:
        return 'Partially covered'
    else:
        return 'Not covered'