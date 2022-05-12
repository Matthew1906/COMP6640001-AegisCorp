from flask_wtf import FlaskForm
from wtforms.fields import DateField, HiddenField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, email, Length

class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), email()])
    password = PasswordField("Password", validators=[InputRequired()])
    sex = SelectField("Sex", choices=['Male', 'Female'], validators=[InputRequired()])
    dob = DateField("Date of Birth", validators=[InputRequired()])
    pob = StringField("Place of Birth")
    marital_status = SelectField("Marital Status", choices=['Single', 'Married'], validators=[InputRequired()])
    mother_name = StringField("Mother's Name", validators=[InputRequired()])
    phone = StringField("Phone Number (with area code)", validators=[InputRequired(), Length(min=10, max=12)])
    address = TextAreaField("Address", validators=[InputRequired()])
    image_url = StringField("Profile Picture Link")
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
