from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired

class InsuranceForm(FlaskForm):
    insurance_id = StringField("Enter Membership Id")
    submit = SubmitField("Register Insurance Policy")
    