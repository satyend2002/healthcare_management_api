from models.doctor import Doctor
from repositories.doctor_repository import DoctorRepository


class DoctorService:

    # Create doctor
    @staticmethod
    def create_doctor(data):

        # Check duplicate phone
        existing_phone = DoctorRepository.get_by_phone(
            data["phone"]
        )

        if existing_phone:
            return {
                "error": "Phone number already exists"
            }, 409

        # Check duplicate email
        existing_email = DoctorRepository.get_by_email(
            data["email"]
        )

        if existing_email:
            return {
                "error": "Email already exists"
            }, 409

        # Create Doctor object
        doctor = Doctor(
            first_name=data["first_name"],
            last_name=data["last_name"],
            specialization=data["specialization"],
            phone=data["phone"],
            email=data["email"],
            department_id=data["department_id"]
        )

        # Save doctor
        doctor = DoctorRepository.create(doctor)

        return doctor


    # Get all doctors
    @staticmethod
    def get_all_doctors(
        page=1,
        per_page=10,
        search="",
        specialization="",
        sort_by="id",
        order="asc"
    ):
        return DoctorRepository.get_all(
            page=page,
            per_page=per_page,
            search=search,
            specialization=specialization,
            sort_by=sort_by,
            order=order
        )

    # Get doctor by ID
    @staticmethod
    def get_doctor(doctor_id):

        doctor = DoctorRepository.get_by_id(doctor_id)

        return doctor


    # Update doctor
    @staticmethod
    def update_doctor(doctor_id, data):

        # Find doctor
        doctor = DoctorRepository.get_by_id(doctor_id)

        if not doctor:
            return {
                "message": "Doctor not found"
            }, 404

        # Check duplicate email
        if "email" in data:

            existing_email = (
                DoctorRepository.get_by_email_excluding_id(
                    data["email"],
                    doctor_id
                )
            )

            if existing_email:
                return {
                    "message": "Email already exists"
                }, 409

        # Check duplicate phone
        if "phone" in data:

            existing_phone = (
                DoctorRepository.get_by_phone_excluding_id(
                    data["phone"],
                    doctor_id
                )
            )

            if existing_phone:
                return {
                    "message": "Phone number already exists"
                }, 409

        # Update fields
        if "first_name" in data:
            doctor.first_name = data["first_name"]

        if "last_name" in data:
            doctor.last_name = data["last_name"]

        if "specialization" in data:
            doctor.specialization = data["specialization"]

        if "phone" in data:
            doctor.phone = data["phone"]

        if "email" in data:
            doctor.email = data["email"]

        if "department_id" in data:
            doctor.department_id = data["department_id"]

        # Save updated doctor
        DoctorRepository.update(doctor)

        return doctor


    # Delete doctor
    @staticmethod
    def delete_doctor(doctor_id):

        doctor = DoctorRepository.get_by_id(doctor_id)

        if not doctor:
            return {
                "message": "Doctor not found"
            }, 404

        DoctorRepository.delete(doctor)

        return {
            "message": "Doctor deleted successfully"
        }, 200