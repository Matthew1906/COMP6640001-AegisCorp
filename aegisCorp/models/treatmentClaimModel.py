# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config tables
class TreatmentClaim(db.Model):
    __tablename__ = 'treatmentClaims'
    policy_id = db.Column(db.Integer, db.ForeignKey('customerInsurances.policy_id'), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('customerInsurances.member_id'), primary_key=True)
    policy = relationship("CustomerInsurance", foreign_keys=[policy_id])
    member = relationship("CustomerInsurance", foreign_keys=[member_id])
    treatment = relationship("TreatmentHeader", back_populates='claims')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentHeaders.id'), primary_key=True)
    claim_status = db.Column(db.Boolean, nullable=False)
    claim_report = db.Column(db.String(2000), unique=True, nullable=False)