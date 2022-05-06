# Database
from .. import db 
from sqlalchemy.orm import relationship 

# Config tables
class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    staffs = relationship("HospitalStaff", back_populates='hospital')
    doctors = relationship("Doctor", back_populates='hospital')
    treatments = relationship("TreatmentHeader", back_populates='hospital')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    hospital = relationship('Hospital', back_populates='doctors')
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"))
    name = db.Column(db.String(255), unique=True, nullable=False)
    treatments = relationship("TreatmentDetail", back_populates='doctor')

class TreatmentHeader(db.Model):
    __tablename__ = 'treatmentHeaders'
    id = db.Column(db.Integer, primary_key=True)
    hospital = relationship('Hospital', back_populates='treatments')
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"))
    customer = relationship("Customer", back_populates='treatments')
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    description = db.Column(db.String(500), unique=True, nullable=False)
    claims = relationship('TreatmentClaim', back_populates='treatment')
    details = relationship("TreatmentDetail", back_populates='header')

class TreatmentDetail(db.Model):
    __tablename__ = 'treatmentDetails'
    id = db.Column(db.Integer, primary_key=True)
    header = relationship("TreatmentHeader", back_populates='details')
    header_id = db.Column(db.Integer, db.ForeignKey("treatmentHeaders.id"))
    doctor = relationship("Doctor", back_populates='treatments')
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    medications = relationship("MedicationDetail", back_populates="treatment")
    check_ups = relationship("CheckUp", back_populates='treatment')
    procedures = relationship("ProcedureDetail", back_populates='treatment')

class CheckUp(db.Model):
    __tablename__ = 'checkups'
    id = db.Column(db.Integer, primary_key=True)
    treatment = relationship("TreatmentDetail", back_populates='checkups')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentDetails.id'), primary_key=True)
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
    treatment = relationship("TreatmentDetail", back_populates='medications')
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
    treatment = relationship("TreatmentDetail", back_populates='procedures')
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatmentDetails.id'), primary_key=True)

class ProcedureType(db.Model):
    __tablename__ = 'procedureTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    procedures = relationship("Procedure", back_populates='type')