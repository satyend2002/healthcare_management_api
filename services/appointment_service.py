from models.appointment import Appointment
from repositories.appointment_repository import AppointmentRepository
from models.patient import Patient
from models.doctor import Doctor


class AppointmentService:

    @staticmethod
    def create(data):
        patient = Patient.query.get(data["patient_id"])

        if not patient:
            raise ValueError("Patient not found")

        doctor = Doctor.query.get(data["doctor_id"])

        if not doctor:
            raise ValueError("Doctor not found")

        appointment = Appointment(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            reason=data.get("reason"),
            status=data.get("status", "scheduled")
        )

        return AppointmentRepository.create(appointment)

    @staticmethod
    def get_by_id(appointment_id):
        appointment = AppointmentRepository.get_by_id(appointment_id)

        if not appointment:
            raise ValueError("Appointment not found")

        return appointment

    @staticmethod
    def get_all(page=1,per_page=10, search="",status="",sort_by="id",order="asc"):
        return AppointmentRepository.get_all(
            page=page,
            per_page=per_page,
            search=search,
            status=status,
            sort_by=sort_by,
            order=order
        )

    @staticmethod
    def update(appointment_id, data):
        appointment = AppointmentService.get_by_id(appointment_id)

        if "patient_id" in data:
            patient = Patient.query.get(data["patient_id"])

            if not patient:
                raise ValueError("Patient not found")

            appointment.patient_id = data["patient_id"]

        if "doctor_id" in data:
            doctor = Doctor.query.get(data["doctor_id"])

            if not doctor:
                raise ValueError("Doctor not found")

            appointment.doctor_id = data["doctor_id"]

        if "appointment_date" in data:
            appointment.appointment_date = data["appointment_date"]

        if "appointment_time" in data:
            appointment.appointment_time = data["appointment_time"]

        if "reason" in data:
            appointment.reason = data["reason"]

        if "status" in data:
            appointment.status = data["status"]

        return AppointmentRepository.update(appointment)

    @staticmethod
    def delete(appointment_id):
        appointment = AppointmentService.get_by_id(appointment_id)

        AppointmentRepository.delete(appointment)

        return True