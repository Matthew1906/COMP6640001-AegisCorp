from datetime import datetime
from flask import Blueprint

utils = Blueprint('utils', __name__)

def currency(price:int):
    price_str = str(price)
    prefix_index = len(price_str)%3 if len(price_str)%3!=0 else 3
    prefix = price_str[:prefix_index]
    suffix = price_str[prefix_index:]
    return 'Rp' + prefix +''.join(["." + suffix[i*3:3*i+3] for i in range(len(price_str)//3) if suffix[i*3:i*3+3]!='']) + ',00'

@utils.app_template_filter('format_date')
def format_date(date):
    return date.strftime("%d/%m/%Y")

@utils.app_template_filter('format_age')
def format_age(date):
    return datetime.now().year - date.year

@utils.app_template_filter('format_marital_status')
def format_marital_status(status):
    return "Married" if status else "Single"

@utils.app_template_filter('format_gender')
def format_gender(status):
    return "♂" if status else '♀'

@utils.app_template_filter('get_treatment_type')
def get_treatment_type(detail):
    if detail.medication != []:
        return "Medication"
    elif detail.checkup != []:
        return "Medical Checkup"
    else: 
        return "Medical Procedure"

@utils.app_template_filter('get_treatment_detail')
def get_treatment_detail(detail):
    if detail.medication != []:
        return detail.medication[0].medication.name + f" x{detail.medication[0].dosage}"
    elif detail.checkup != []:
        return detail.checkup[0].diagnosis
    else: 
        return detail.procedure[0].procedure.name

@utils.app_template_filter('get_treatment_cost')
def get_treatment_cost(detail):
    if detail.medication != []:
        return currency(detail.medication[0].medication.price * detail.medication[0].dosage * 15000)
    elif detail.checkup != []:
        return currency(detail.checkup[0].price)
    else: 
        return currency(detail.procedure[0].procedure.price * 15000)

@utils.app_template_filter('get_treatment_status')
def get_treatment_status(detail):
    return "Completed" if datetime.now()>detail.endDate else "Ongoing"

@utils.app_template_filter('get_treatment_type_lower')
def get_treatment_type(detail):
    if detail.medication != []:
        return "medication"
    elif detail.checkup != []:
        return "checkup"
    else: 
        return "procedure"

@utils.app_template_filter('add_args')
def add_args(detail):
    return f"&search={detail}" if detail else ""

@utils.app_template_filter('get_first_date')
def get_first_date(details):
    if details == []:
        return "No Treatment Registered"
    else:
        first_date = details[0].startDate
        for detail in details:
            if detail.startDate<first_date:
                first_date = detail.startDate
        return format_date(first_date)