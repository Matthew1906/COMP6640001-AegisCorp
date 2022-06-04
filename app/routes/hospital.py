from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .. import db
from ..forms import CheckUpForm, MedicationForm, MedicalProcedureForm,\
    TreatmentForm
from ..models import Customer, CustomerInsurance, Doctor, HospitalStaff,\
    TreatmentClaim, TreatmentHeader, TreatmentDetail, CheckUp, Medication,\
        Procedure, MedicationDetail, ProcedureDetail
from ..utils import hospital_only

hospital = Blueprint("hospital", __name__)

@hospital.route("/treatments/add", methods=['GET','POST'])
@hospital_only
def add_treatment():
    form = TreatmentForm(customers=[(customer.id, customer.user.name) for customer in Customer.query.all()])
    staff = HospitalStaff.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        new_treatment = TreatmentHeader(
            hospital_id = staff.hospital_id,
            customer_id = int(request.form.get('customer')),
            description = request.form.get('description')
        )
        db.session.add(new_treatment)
        db.session.commit()
        return redirect(url_for('views.home'))
    else:
        return render_template('treatment.html', form=form, purpose='add', hospital=staff.hospital_id)

@hospital.route('/treatments/<int:treatment_id>')
@login_required
def get_treatment(treatment_id:int):
    treatment = TreatmentHeader.query.filter_by(id=treatment_id).first()
    details = TreatmentDetail.query.filter_by(header_id=treatment.id).order_by(TreatmentDetail.startDate.desc())
    detail_filters = {
        'all':details,
        'checkup':details.join(TreatmentDetail.checkup),
        'medication':details.join(TreatmentDetail.medication),
        'procedure':details.join(TreatmentDetail.procedure)
    }
    details = detail_filters.get(request.args.get('type','all'))
    insurances = CustomerInsurance.query.filter_by(member_id=treatment.customer_id)
    claim = TreatmentClaim.query.filter_by(member_id=treatment.customer_id, treatment_id=treatment.id).first() if(request.args.get('claim')!=None) else None
    return render_template('treatment.html', purpose='show', treatment=treatment, details=details, insurances=insurances, claim=claim)

@hospital.route("/treatments/<int:treatment_id>/add/<type>", methods=['GET','POST'])
@hospital_only
def add_detail(treatment_id:int, type:str=None):
    treatment = TreatmentHeader.query.filter_by(id=treatment_id).first()
    medications = Medication.query.all()
    procedures = Procedure.query.all()
    doctors = [(doctor.id, doctor.name) for doctor in Doctor.query.filter_by(hospital_id = treatment.hospital_id)]
    detail_forms = {
        'medication':MedicationForm(
            doctors = doctors,
            options = [(medication.id, medication.name) for medication in medications]
        ), 
        'checkup':CheckUpForm(doctors = doctors), 
        'procedure':MedicalProcedureForm(
            doctors = doctors,
            options = [(procedure.id,procedure.name) for procedure in procedures]
        )
    }
    form = detail_forms.get(type)
    if form.validate_on_submit():
        new_detail = TreatmentDetail(
            header_id = treatment.id,
            doctor_id = int(request.form.get('doctor')),
            startDate = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d"),
            endDate = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d")
        )        
        db.session.add(new_detail)
        db.session.commit()
        if type == 'medication':
            new_meds = MedicationDetail(
                medication_id = request.form.get('name'),
                treatment_id = new_detail.id,
                dosage = int(request.form.get('dosage'))
            )
            db.session.add(new_meds)
        elif type == 'checkup':
            new_checkup = CheckUp(
                treatment_id = new_detail.id,
                diagnosis = request.form.get('diagnosis'),
                price = int(request.form.get('price'))
            )
            db.session.add(new_checkup)
        else: 
            new_procedure = ProcedureDetail(
                procedure_id = int(request.form.get('name')),
                treatment_id = new_detail.id
            )
            db.session.add(new_procedure)
        db.session.commit()
        return redirect(url_for('hospital.get_treatment', treatment_id=treatment.id))
    else:
        return render_template('treatment.html', purpose='add_detail', form=form, treatment = treatment, type=type)

@hospital.route("/treatments/<int:treatment_id>/update/<type>/<int:detail_id>", methods=['GET','POST'])
@hospital_only
def update_detail(treatment_id:int, type:str, detail_id:int):
    find_detail = TreatmentDetail.query.filter_by(id=detail_id).first()
    medications = Medication.query.all()
    procedures = Procedure.query.all()
    doctors = [(doctor.id, doctor.name) for doctor in Doctor.query.filter_by(hospital_id = find_detail.header.hospital_id)]
    if type == 'medication':
        find_meds = MedicationDetail.query.filter_by(treatment_id=detail_id).first()
        form = MedicationForm(
            doctors = doctors,
            options = [(medication.id, medication.name) for medication in medications],
            start_date = find_detail.startDate,
            end_date = find_detail.endDate,
            dosage = find_meds.dosage
        )
        if form.validate_on_submit():
            find_detail.doctor_id = int(request.form.get('doctor'))
            find_detail.startDate = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d")
            find_detail.endDate = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d")
            find_meds.medication_id = request.form.get('name')
            find_meds.dosage = int(request.form.get('dosage'))
            db.session.commit()
            return redirect(url_for('hospital.get_treatment', treatment_id=treatment_id))
    elif type == 'checkup':
        find_checkup = CheckUp.query.filter_by(treatment_id=detail_id).first()
        form = CheckUpForm(
            doctors = doctors,
            start_date = find_detail.startDate,
            end_date = find_detail.endDate,
            diagnosis = find_checkup.diagnosis,
            price = find_checkup.price
        )
        if form.validate_on_submit():
            find_detail.doctor_id = int(request.form.get('doctor'))
            find_detail.startDate = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d")
            find_detail.endDate = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d")
            find_checkup.diagnosis = request.form.get('diagnosis')
            find_checkup.price = request.form.get('price')
            db.session.commit()
            return redirect(url_for('hospital.get_treatment', treatment_id=treatment_id))
    elif type == 'procedure':
        find_procedure = ProcedureDetail.query.filter_by(treatment_id=detail_id).first()
        form = MedicalProcedureForm(
            doctors = doctors,
            options = [(procedure.id,procedure.name) for procedure in procedures],
            start_date = find_detail.startDate,
            end_date = find_detail.endDate,
        )
        if form.validate_on_submit():
            find_detail.doctor_id = int(request.form.get('doctor')),
            find_detail.startDate = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d"),
            find_detail.endDate = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d")
            find_procedure.procedure_id = int(request.form.get('name')),
            db.session.commit()
            return redirect(url_for('hospital.get_treatment', treatment_id=treatment_id))
    return render_template('treatment.html', purpose='edit_detail', form=form, treatment = find_detail.header, type=type, detail=find_detail)

@hospital.route("/treatments/<int:treatment_id>/delete/<type>/<int:detail_id>", methods=['POST'])
@hospital_only
def delete_detail(treatment_id:int, type:str, detail_id:int):
    type_models = {'medication':MedicationDetail, 'checkup':CheckUp, 'procedure':ProcedureDetail}
    find_type = type_models.get(type).query.filter_by(treatment_id=detail_id).first()
    if find_type:
        db.session.delete(find_type)
        db.session.commit()
    find_detail = TreatmentDetail.query.filter_by(id=detail_id).first()
    if find_detail:
        db.session.delete(find_detail)
        db.session.commit()  
    return redirect(url_for('hospital.get_treatment', treatment_id=treatment_id))