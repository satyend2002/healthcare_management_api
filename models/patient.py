from datetime import datetime

from extensions.extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

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

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    gender = db.Column(
        db.String(20),
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

    address = db.Column(
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

    appointments = db.relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan"
    ) 
    
    prescriptions = db.relationship(
    "Prescription",
    back_populates="patient"
)
    