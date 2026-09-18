from datetime import datetime
from extensions.extensions import db


class Medicine(db.Model):
    __tablename__ = "medicines"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    generic_name = db.Column(db.String(255),nullable=True)
    
    brand_name = db.Column(db.String(255),nullable=True)
    strength = db.Column(db.String(100),nullable=True)
    dosage_form = db.Column(db.String(100),nullable=True)
    
    manufacturer = db.Column(db.String(255),nullable=True)
    stock_quantity = db.Column(db.Integer,nullable=False,default=0)
    reorder_level = db.Column(db.Integer,nullable=False,default=10)

    active = db.Column(db.Boolean,nullable=False,default=True)

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
    
    prescription_items = db.relationship(
        "PrescriptionItem",
        back_populates="medicine"
    )