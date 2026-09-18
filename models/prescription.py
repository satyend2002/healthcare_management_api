from datetime import datetime

from extensions.extensions import db


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=False
    )

    medicine_name = db.Column(
        db.String(255),
        nullable=False
    )

    dosage = db.Column(
        db.String(100),
        nullable=False
    )

    frequency = db.Column(
        db.String(100),
        nullable=False
    )

    duration = db.Column(
        db.String(100),
        nullable=False
    )

    instructions = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    patient = db.relationship(
        "Patient",
        back_populates="prescriptions"
    )

    doctor = db.relationship(
        "Doctor",
        back_populates="prescriptions"
    )

    appointment = db.relationship(
        "Appointment",
        back_populates="prescriptions"
    )
    
    items = db.relationship(
        "PrescriptionItem",
        back_populates="prescription",
        cascade="all, delete-orphan"
    )