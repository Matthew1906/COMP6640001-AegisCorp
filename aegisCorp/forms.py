from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField , PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import InputRequired, email, NumberRange