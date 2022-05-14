from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
from ..forms import RegisterForm, LoginForm
from ..models import User, Customer, HospitalStaff, InsuranceStaff
from ..utils.image_processing import get_image_url

auth = Blueprint("auth", __name__)

# Utilities
def get_user_by_email(model, email):
    return User.query.join(model).filter(User.email==email).first()

@auth.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        find_user = User.query.filter_by(email=email).first()
        if find_user == None:
            new_user = User(
                name = request.form.get('name'),
                email = email,
                password = generate_password_hash(
                    request.form.get('password'),
                    method='pbkdf2:sha256',
                    salt_length=9,
                ),
                sex = 1 if request.form.get('sex') == 'Male' else 0,
                dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d")
            )
            db.session.add(new_user)
            db.session.commit()
            new_customer = Customer(
                user_id = new_user.id,
                pob = request.form.get('pob'),
                marital_status = 1 if request.form.get('marital_status') == 'Married' else 0,
                mother_name = request.form.get('mother_name'),
                phone = request.form.get('phone'),
                address = request.form.get('address'),
                image_url = get_image_url(request.files['image'].read(), new_user.name.lower().split()[0]+ str(new_user.id) +'.jpg') \
                    if 'image' in request.files and request.files['image'].filename !='' \
                    else 'https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png'
            )
            db.session.add(new_customer)
            db.session.commit()
            flash('Registration completed! Login now!')
        else:
            flash("Customer is already registered! Login Now")
        return redirect(url_for("auth.login"))   
    return render_template("auth.html", form=form, purpose='register')

@auth.route("/login", methods=['GET','POST'])
def login():
    user_type = request.form.get('type')
    form = LoginForm()
    if user_type==None:
        return render_template("auth.html", form = form, purpose='login')
    elif form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get('password')
        user_models={'Customer':Customer, 'Hospital':HospitalStaff, 'Insurance':InsuranceStaff}
        find_user = get_user_by_email(user_models.get(user_type), email)
        if find_user!=None:
            if check_password_hash(find_user.password, password):
                login_user(find_user)
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password! Try again!")
                return redirect(url_for('auth.login'))
        elif user_type=='Customer':
            flash("You need to register first as a customer!")
            return redirect(url_for("auth.register"))
        else:
            staff_type = 'a ' + user_type if user_type == 'Hospital' else 'an ' + user_type
            flash(f"You aren't registered as {staff_type} Staff! Please try inputting the correct credentials!")
            return redirect(url_for('auth.login'))

@login_required
@auth.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('views.home'))