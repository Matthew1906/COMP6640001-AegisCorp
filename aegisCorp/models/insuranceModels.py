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
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), primary_key=True)
    policy = relationship("InsurancePolicy", back_populates='customer_insurances')
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), primary_key=True)
    expiration_date = db.Column(db.DateTime, nullable=False)
    treatment_claims = relationship("TreatmentClaim", back_populates='customer_insurance')

class TreatmentClaim(db.Model):
    __tablename__ = 'treatmentClaims'
    customer_insurance = relationship("CustomerInsurance", back_populates='treatment_claims')
    policy_id = db.Column(db.Integer, db.ForeignKey('customerInsurances.policy_id'), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('customerInsurances.member_id'), primary_key=True)
    treatment = relationship("TreatmentHeader", back_populates='claims')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentHeaders.id'), primary_key=True)
    claim_status = db.Column(db.Boolean, nullable=False)
    claim_report = db.Column(db.String(2000), unique=True, nullable=False)