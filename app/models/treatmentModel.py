from sqlalchemy.orm import relationship 
from .. import db 

# Config tables
class CheckUp(db.Model):
    __tablename__ = 'checkups'
    id = db.Column(db.Integer, primary_key=True)
    treatment = relationship("TreatmentDetail", back_populates='checkup')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentDetails.id'))
    diagnosis = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Medication(db.Model):
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    details = relationship("MedicationDetail", back_populates='medication')

class MedicationDetail(db.Model):
    __tablename__ = 'medicationDetails'
    medication = relationship("Medication", back_populates='details')
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"), primary_key=True)
    treatment = relationship("TreatmentDetail", back_populates='medication')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentDetails.id'), primary_key=True)
    dosage = db.Column(db.Integer, nullable=False)

class Procedure(db.Model):
    __tablename__ = 'procedures'
    id = db.Column(db.Integer, primary_key=True)
    type = relationship('ProcedureType', back_populates='procedures')
    type_id = db.Column(db.Integer, db.ForeignKey('procedureTypes.id'))
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    details = relationship('ProcedureDetail', back_populates='procedure')

class ProcedureDetail(db.Model):
    __tablename__ = 'procedureDetails'
    procedure = relationship("Procedure", back_populates='details')
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id'), primary_key=True)
    treatment = relationship("TreatmentDetail", back_populates='procedure')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentDetails.id'), primary_key=True)

class ProcedureType(db.Model):
    __tablename__ = 'procedureTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    procedures = relationship("Procedure", back_populates='type')