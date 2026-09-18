from datetime import datetime

from extensions.extensions import db


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )
    

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=True
    )

    subtotal = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    tax = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    discount = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    total_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    due_date = db.Column(
        db.Date,
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