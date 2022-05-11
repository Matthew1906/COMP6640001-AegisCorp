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
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
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
    checkups = relationship("CheckUp", back_populates='treatment')
    procedures = relationship("ProcedureDetail", back_populates='treatment')