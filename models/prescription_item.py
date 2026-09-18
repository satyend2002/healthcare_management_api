from datetime import datetime

from extensions.extensions import db


class PrescriptionItem(db.Model):
    __tablename__ = "prescription_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    prescription_id = db.Column(
        db.Integer,
        db.ForeignKey("prescriptions.id"),
        nullable=False
    )

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id"),
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

    prescription = db.relationship(
        "Prescription",
        back_populates="items"
    )

    medicine = db.relationship(
        "Medicine",
        back_populates="prescription_items"
    )