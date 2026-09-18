from datetime import datetime
from extensions.extensions import db


class LabTest(db.Model):
    __tablename__ = "lab_tests"

    id = db.Column(db.Integer, primary_key=True)

    test_code = db.Column(db.String(50),unique=True,nullable=False)

    test_name = db.Column(db.String(255),nullable=False)

    description = db.Column(db.String(1000),nullable=True)

    sample_type = db.Column(db.String(100),nullable=True)

    price = db.Column(db.Numeric(10, 2),nullable=False,default=0)

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