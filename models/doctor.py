from datetime import datetime

from extensions.extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
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

    appointments = db.relationship(
        "Appointment",
        back_populates="doctor"
    )

    department = db.relationship(
        "Department",
        back_populates="doctors"
    )
    
    prescriptions = db.relationship(
    "Prescription",
    back_populates="doctor"
    )