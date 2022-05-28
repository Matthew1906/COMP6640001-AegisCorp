from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField
from wtforms.validators import InputRequired

class InsuranceForm(FlaskForm):
    company = SelectField("Insurance Company", validators=[InputRequired()])
    policy = SelectField("Insurance Policy", validators=[InputRequired()])
    submit = SubmitField("Add New Insurance Policy")