from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import DateField, FileField, HiddenField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, email, Length
from ..models import Customer

class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), email()])
    password = PasswordField("Password", validators=[InputRequired()])
    sex = SelectField("Sex", choices=['Male', 'Female'], validators=[InputRequired()])
    dob = DateField("Date of Birth", validators=[InputRequired()])
    pob = StringField("Place of Birth")
    marital_status = SelectField("Marital Status", choices=['Single', 'Married'], validators=[InputRequired()])
    mother_name = StringField("Mother's Name", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[InputRequired(), Length(min=10, max=12)])
    address = TextAreaField("Address", validators=[InputRequired()])
    image = FileField("Profile Picture", validators=[FileAllowed(['jpg','png'], 'Images only!')])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), email()])
    password = PasswordField("Password", validators=[InputRequired()])
    type = SelectField(
        label = "Type", 
        choices = [
            ('Customer', 'customer'), 
            ('Hospital', 'hospital'),
            ('Insurance', 'insurance')
        ], 
        validators = [InputRequired()])
    submit = SubmitField("Login")

class TreatmentForm(FlaskForm):
    hospital = HiddenField(label='Hospital')
    customer = SelectField(label='Patient Name')
    description = StringField(label='Treatment Description', validators=[InputRequired()])
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