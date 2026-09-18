from extensions.extensions import db
from models.doctor import Doctor
from sqlalchemy import or_


class DoctorRepository:

    # Get all doctors
    @staticmethod
    def get_all(
        page=1,
        per_page=10,
        search="",
        specialization="",
        sort_by="id",
        order="asc"
    ):
        query = Doctor.query

        # Search by name, phone, or email
        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    Doctor.first_name.ilike(search_pattern),
                    Doctor.last_name.ilike(search_pattern),
                    Doctor.phone.ilike(search_pattern),
                    Doctor.email.ilike(search_pattern)
                )
            )

        # Filter by specialization
        if specialization:
            query = query.filter(
                Doctor.specialization.ilike(specialization)
            )

        # Allowed sorting fields
        allowed_sort_fields = {
            "id": Doctor.id,
            "first_name": Doctor.first_name,
            "last_name": Doctor.last_name,
            "specialization": Doctor.specialization,
            "created_at": Doctor.created_at
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Doctor.id
        )

        # Apply sorting
        if order == "desc":
            query = query.order_by(
                sort_column.desc(),
                Doctor.id.desc()
            )
        else:
            query = query.order_by(
                sort_column.asc(),
                Doctor.id.asc()
            )

        # Apply pagination
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )


    # Get doctor by ID .............................
    @staticmethod
    def get_by_id(doctor_id):
        return db.session.get(Doctor, doctor_id)


    # Get doctor by phone .................
    @staticmethod
    def get_by_phone(phone):
        return Doctor.query.filter_by(
            phone=phone
        ).first()


    # Get doctor by email .................................
    @staticmethod
    def get_by_email(email):
        return Doctor.query.filter_by(
            email=email
        ).first()


    # Get doctor by email excluding current doctor .......
    @staticmethod
    def get_by_email_excluding_id(email, doctor_id):
        return Doctor.query.filter(
            Doctor.email == email,
            Doctor.id != doctor_id
        ).first()


    # Get doctor by phone excluding current doctor ..........
    @staticmethod
    def get_by_phone_excluding_id(phone, doctor_id):
        return Doctor.query.filter(
            Doctor.phone == phone,
            Doctor.id != doctor_id
        ).first()


    # Create doctor  ...............
    @staticmethod
    def create(doctor):
        db.session.add(doctor)
        db.session.commit()

        return doctor


    # Update doctor ...............
    @staticmethod
    def update(doctor):
        db.session.commit()
        return doctor 


    # Delete doctor ..................
    @staticmethod
    def delete(doctor):
        db.session.delete(doctor)
        db.session.commit()