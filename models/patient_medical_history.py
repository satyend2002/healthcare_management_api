from datetime import datetime

from extensions.extensions import db


class PatientMedicalHistory(db.Model):
    __tablename__ = "patient_medical_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    history_type = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.String(2000),
        nullable=False
    )

    diagnosis_date = db.Column(
        db.Date,
        nullable=True
    )

    notes = db.Column(
        db.String(2000),
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