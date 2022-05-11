# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config tables
class InsuranceCompany(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    staffs = relationship("InsuranceStaff", back_populates='company')
    policies = relationship("InsurancePolicy", back_populates='company')

class InsurancePolicy(db.Model):
    __tablename__ = 'policies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    company = relationship("InsuranceCompany", back_populates='policies')
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
    benefits = db.Column(db.String(2000), nullable=False)
    customer_insurances = relationship("CustomerInsurance", back_populates='policy')

class CustomerInsurance(db.Model):
    __tablename__ = 'customerInsurances'
    member = relationship("Customer", back_populates='insurances')
    member_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    policy = relationship("InsurancePolicy", back_populates='customer_insurances')
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), primary_key=True)
    expiration_date = db.Column(db.DateTime, nullable=False)