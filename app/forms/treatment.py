from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import DateField, FileField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

class TreatmentForm(FlaskForm):
    hospital = HiddenField(label='Hospital')
    customer = SelectField(label='Patient Name')
    description = StringField(label='Treatment Description', validators=[InputRequired()])
    identity = FileField(label='Identity Confirmation', validators=[FileAllowed(['jpg','png'], 'Images only!')])
    submit = SubmitField(label='Add New Treatment')
    def __init__(self, customers = [], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer.choices = customers

class TreatmentDetailForm(FlaskForm):
    doctor = SelectField("Doctor")
    start_date = DateField("Treatment Start Date", validators=[InputRequired()])
    end_date = DateField("Treatment End Date", validators=[InputRequired()])
    submit = SubmitField("Add Detail")
    def __init__(self, doctors=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doctor.choices = doctors

class MedicationForm(TreatmentDetailForm):
    name = SelectField("Medication Name")
    dosage = IntegerField("Dosage", validators=[InputRequired()])
    def __init__(self, options=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name.choices = options

class CheckUpForm(TreatmentDetailForm):
    diagnosis = TextAreaField("Diagnosis", validators=[InputRequired()])
    price = IntegerField("Price (in Rupiah)", validators=[InputRequired()])

class MedicalProcedureForm(TreatmentDetailForm):
    name = SelectField("Procedure Name")
    def __init__(self, options=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name.choices = options