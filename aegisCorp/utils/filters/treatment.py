from datetime import datetime
from .utils import currency 

def get_treatment_type(detail):
    if detail.medication != []:
        return "Medication"
    elif detail.checkup != []:
        return "Medical Checkup"
    else: 
        return "Medical Procedure"

def get_treatment_detail(detail):
    if detail.medication != []:
        return detail.medication[0].medication.name + f" x{detail.medication[0].dosage}"
    elif detail.checkup != []:
        return detail.checkup[0].diagnosis
    else: 
        return detail.procedure[0].procedure.name

def get_treatment_cost(detail):
    if detail.medication != []:
        return currency(detail.medication[0].medication.price * detail.medication[0].dosage * 15000)
    elif detail.checkup != []:
        return currency(detail.checkup[0].price)
    else: 
        return currency(detail.procedure[0].procedure.price * 15000)

def get_treatment_status(detail):
    return "Completed" if datetime.now()>detail.endDate else "Ongoing"

def get_treatment_type_lower(detail):
    if detail.medication != []:
        return "medication"
    elif detail.checkup != []:
        return "checkup"
    else: 
        return "procedure"

def add_args(detail):
    return f"&search={detail}" if detail else ""

def get_first_date(details):
    if details == []:
        return "No Treatment Registered"
    else:
        first_date = details[0].startDate
        for detail in details:
            if detail.startDate<first_date:
                first_date = detail.startDate
        return format_date(first_date)
