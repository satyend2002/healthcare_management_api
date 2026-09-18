from models.appointment import Appointment
from extensions.extensions import db
from sqlalchemy import or_

class AppointmentRepository:

    @staticmethod
    def create(appointment):
        db.session.add(appointment)
        db.session.commit()
        return appointment

    @staticmethod
    def get_by_id(appointment_id):
        return Appointment.query.get(appointment_id)

    @staticmethod
    def get_all(
        page=1,
        per_page=10,
        search="",
        status="",
        sort_by="id",
        order="asc"
    ):
        query = Appointment.query

        # Search by appointment reason .....
        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    Appointment.reason.ilike(search_pattern),
                    Appointment.status.ilike(search_pattern)
                )
            )

        # Filter by appointment status .....
        if status:
            query = query.filter(
                Appointment.status.ilike(status)
            )

        # Allowed sorting fields ......
        allowed_sort_fields = {
            "id": Appointment.id,
            "appointment_date": Appointment.appointment_date,
            "appointment_time": Appointment.appointment_time,
            "status": Appointment.status,
            "created_at": Appointment.created_at
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Appointment.id
        )

        # Apply sorting with stable secondary sorting ...
        if order == "desc":
            query = query.order_by(
                sort_column.desc(),
                Appointment.id.desc()
            )
            
        else:
            query = query.order_by(
                sort_column.asc(),
                Appointment.id.asc()
            )

        # Apply pagination
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def update(appointment):
        db.session.commit()
        return appointment

    @staticmethod
    def delete(appointment):
        db.session.delete(appointment)
        db.session.commit()