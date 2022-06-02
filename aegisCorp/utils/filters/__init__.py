from flask import Blueprint
from .utils import format_date
from .insurance import *
from .treatment import *
from .user import *

utils = Blueprint('utils', __name__)

# Get Type
utils.add_app_template_filter(get_user_type, 'get_user_type')
utils.add_app_template_filter(get_treatment_type, 'get_treatment_type')
utils.add_app_template_filter(get_treatment_type_lower, 'get_treatment_type_lower')

# Formatting value
utils.add_app_template_filter(format_date, 'format_date')
utils.add_app_template_filter(format_age, 'format_age')
utils.add_app_template_filter(format_marital_status, 'format_marital_status')
utils.add_app_template_filter(format_gender, 'format_gender')
utils.add_app_template_filter(format_insurance_id, 'format_insurance_id')

# Get value
utils.add_app_template_filter(get_treatment_cost, 'get_treatment_cost')
utils.add_app_template_filter(get_treatment_detail, 'get_treatment_detail')
utils.add_app_template_filter(get_treatment_status, 'get_treatment_status')
utils.add_app_template_filter(get_first_date, 'get_first_date')
utils.add_app_template_filter(get_insurance_benefits, 'get_insurance_benefits')
utils.add_app_template_filter(get_insurance_company, 'get_insurance_company')
utils.add_app_template_filter(get_insurance_policy, 'get_insurance_policy')

# URL Manipulation
utils.add_app_template_filter(add_args, 'add_args')
