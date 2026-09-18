# from datetime import datetime

# from extensions.extensions import db


# class Appointment(db.Model):
#     __tablename__ = "appointments"

#     id = db.Column(db.Integer,primary_key=True)

#     patient_id = db.Column(db.Integer,db.ForeignKey("patients.id"),nullable=False)

#     doctor_id = db.Column(db.Integer,db.ForeignKey("doctors.id"),nullable=False)

#     appointment_date = db.Column(db.Date,nullable=False)

#     appointment_time = db.Column(db.Time,nullable=False)

#     reason = db.Column(db.String(255),nullable=True)

#     status = db.Column(db.String(20),nullable=False,default="scheduled")

#     created_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

#     updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)


from datetime import datetime

from extensions.extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

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

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    appointment_time = db.Column(
        db.Time,
        nullable=False
    )

    reason = db.Column(
        db.String(255),
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="scheduled"
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
        back_populates="appointments"
    )

    doctor = db.relationship(
        "Doctor",
        back_populates="appointments"
    )
    prescriptions = db.relationship(
    "Prescription",
    back_populates="appointment"
    )