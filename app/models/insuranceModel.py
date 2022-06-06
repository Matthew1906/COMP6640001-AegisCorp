from sqlalchemy.orm import relationship 
from .. import db 

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
    benefits = relationship("PolicyBenefit", back_populates='policy')
    customer_insurances = relationship("CustomerInsurance", back_populates='policy')

class BenefitType(db.Model):
    __tablename__ = 'benefitTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    benefits = relationship("Benefit", back_populates='type')

class Benefit(db.Model):
    __tablename__ = 'benefits'
    id = db.Column(db.Integer, primary_key=True)
    type = relationship("BenefitType", back_populates='benefits')
    type_id = db.Column(db.Integer, db.ForeignKey('benefitTypes.id'))
    price_limit = db.Column(db.Integer, nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    policy_benefits = relationship("PolicyBenefit", back_populates='benefit')

class PolicyBenefit(db.Model):
    __tablename__ = 'policyBenefits'
    policy = relationship("InsurancePolicy", back_populates='benefits')
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), primary_key=True)
    benefit = relationship("Benefit", back_populates='policy_benefits')
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefits.id'), primary_key=True)

class CustomerInsurance(db.Model):
    __tablename__ = 'customerInsurances'
    member = relationship("Customer", back_populates='insurances')
    member_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    policy = relationship("InsurancePolicy", back_populates='customer_insurances')
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), primary_key=True)
    expiration_date = db.Column(db.DateTime, nullable=False)