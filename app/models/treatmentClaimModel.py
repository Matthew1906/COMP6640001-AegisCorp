from sqlalchemy.orm import relationship 
from .. import db 

# Config tables
class TreatmentClaim(db.Model):
    __tablename__ = 'treatmentClaims'
    member = relationship("Customer", back_populates='claims')
    treatment = relationship("TreatmentHeader", back_populates='claims')
    member_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentHeaders.id'), primary_key=True)
    claim_status = db.Column(db.Boolean, nullable=False)
    claim_report = db.Column(db.String(2000), unique=True, nullable=False)
    