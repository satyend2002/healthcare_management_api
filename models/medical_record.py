from datetime import datetime

from extensions.extensions import db


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

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
        nullable=True
    )

    diagnosis = db.Column(
        db.String(500),
        nullable=False
    )

    symptoms = db.Column(
        db.String(1000),
        nullable=True
    )

    treatment = db.Column(
        db.String(1000),
        nullable=True
    )

    notes = db.Column(
        db.String(2000),
        nullable=True
    )

    record_date = db.Column(
        db.Date,
        nullable=False
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
    