from models.medical_record import MedicalRecord
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

from repositories.medical_record_repository import (
    MedicalRecordRepository
)


class MedicalRecordService:

    @staticmethod
    def create(data):
        patient = Patient.query.get(
            data["patient_id"]
        )

        if not patient:
            raise ValueError("Patient not found")

        doctor = Doctor.query.get(
            data["doctor_id"]
        )

        if not doctor:
            raise ValueError("Doctor not found")

        appointment_id = data.get("appointment_id")

        if appointment_id is not None:
            appointment = Appointment.query.get(
                appointment_id
            )

            if not appointment:
                raise ValueError("Appointment not found")

        medical_record = MedicalRecord(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            appointment_id=appointment_id,
            diagnosis=data["diagnosis"],
            symptoms=data.get("symptoms"),
            treatment=data.get("treatment"),
            notes=data.get("notes"),
            record_date=data["record_date"]
        )

        return MedicalRecordRepository.create(
            medical_record
        )

    @staticmethod
    def get_by_id(medical_record_id):
        medical_record = (
            MedicalRecordRepository.get_by_id(
                medical_record_id
            )
        )

        if not medical_record:
            raise ValueError("Medical record not found")

        return medical_record

    @staticmethod
    def get_all():
        return MedicalRecordRepository.get_all()

    @staticmethod
    def get_by_patient_id(patient_id):
        patient = Patient.query.get(patient_id)

        if not patient:
            raise ValueError("Patient not found")

        return MedicalRecordRepository.get_by_patient_id(
            patient_id
        )

    @staticmethod
    def update(medical_record_id, data):
        medical_record = (
            MedicalRecordService.get_by_id(
                medical_record_id
            )
        )

        if "patient_id" in data:
            patient = Patient.query.get(
                data["patient_id"]
            )

            if not patient:
                raise ValueError("Patient not found")

            medical_record.patient_id = data["patient_id"]

        if "doctor_id" in data:
            doctor = Doctor.query.get(
                data["doctor_id"]
            )

            if not doctor:
                raise ValueError("Doctor not found")

            medical_record.doctor_id = data["doctor_id"]

        if "appointment_id" in data:
            appointment_id = data["appointment_id"]

            if appointment_id is not None:
                appointment = Appointment.query.get(
                    appointment_id
                )

                if not appointment:
                    raise ValueError("Appointment not found")

            medical_record.appointment_id = appointment_id

        if "diagnosis" in data:
            medical_record.diagnosis = data["diagnosis"]

        if "symptoms" in data:
            medical_record.symptoms = data["symptoms"]

        if "treatment" in data:
            medical_record.treatment = data["treatment"]

        if "notes" in data:
            medical_record.notes = data["notes"]

        if "record_date" in data:
            medical_record.record_date = data["record_date"]

        return MedicalRecordRepository.update(
            medical_record
        )

    @staticmethod
    def delete(medical_record_id):
        medical_record = (
            MedicalRecordService.get_by_id(
                medical_record_id
            )
        )

        MedicalRecordRepository.delete(
            medical_record
        )

        return True