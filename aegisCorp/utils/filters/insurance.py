from .utils import currency, format_id

def format_insurance_id(insurance):
    return f"MEM_{format_id(insurance.member_id)}_POL_{format_id(insurance.policy_id)}"

def get_insurance_benefits(insurance):
    return [f"Coverage for {benefit.benefit.type.name.capitalize()} \
        with maximum fee of {currency(benefit.benefit.price_limit)} - \
        applicable for age {benefit.benefit.min_age}-{benefit.benefit.max_age}" 
        for benefit in insurance.policy.benefits
    ]
    
def get_insurance_company(insurance):
    return insurance.policy.company.name

def get_insurance_policy(insurance):
    return insurance.policy.name
