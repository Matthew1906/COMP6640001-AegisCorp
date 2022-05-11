# Database
from .. import db 
from sqlalchemy.orm import relationship 
from flask_login import UserMixin

# Config tables
class User(db.Model, UserMixin):
    '''User Table'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.Boolean, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    customers = relationship('Customer', back_populates='user')
    insurance_staffs = relationship('InsuranceStaff', back_populates='user')
    hospital_staffs = relationship('HospitalStaff', back_populates='user')

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user = relationship("User", back_populates='customers')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pob = db.Column(db.String(255))
    marital_status = db.Column(db.Boolean, nullable=False)
    mother_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), unique=True, nullable=False)
    insurances = relationship("CustomerInsurance", back_populates="member")
    treatments = relationship("TreatmentHeader", back_populates='customer')

class InsuranceStaff(db.Model):
    __tablename__ = 'insuranceStaffs'
    user = relationship("User", back_populates='insurance_staffs')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    company = relationship("InsuranceCompany", back_populates='staffs')
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)

class HospitalStaff(db.Model):
    __tablename__ = 'hospitalStaffs'
    user = relationship("User", back_populates='hospital_staffs')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    hospital = relationship("Hospital", back_populates='staffs')
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), primary_key=True)
