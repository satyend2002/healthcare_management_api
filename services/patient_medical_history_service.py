from models.patient_medical_history import PatientMedicalHistory
from models.patient import Patient

from repositories.patient_medical_history_repository import (
    PatientMedicalHistoryRepository
)


class PatientMedicalHistoryService:

    @staticmethod
    def create(data):
        patient = Patient.query.get(
            data["patient_id"]
        )

        if not patient:
            raise ValueError("Patient not found")

        history = PatientMedicalHistory(
            patient_id=data["patient_id"],
            history_type=data["history_type"],
            description=data["description"],
            diagnosis_date=data.get("diagnosis_date"),
            notes=data.get("notes")
        )

        return PatientMedicalHistoryRepository.create(
            history
        )

    @staticmethod
    def get_by_id(history_id):
        history = (
            PatientMedicalHistoryRepository.get_by_id(
                history_id
            )
        )

        if not history:
            raise ValueError(
                "Patient medical history not found"
            )

        return history

    @staticmethod
    def get_all():
        return PatientMedicalHistoryRepository.get_all()

    @staticmethod
    def get_by_patient_id(patient_id):
        patient = Patient.query.get(patient_id)

        if not patient:
            raise ValueError("Patient not found")

        return (
            PatientMedicalHistoryRepository
            .get_by_patient_id(patient_id)
        )

    @staticmethod
    def update(history_id, data):
        history = (
            PatientMedicalHistoryService
            .get_by_id(history_id)
        )

        if "patient_id" in data:
            patient = Patient.query.get(
                data["patient_id"]
            )

            if not patient:
                raise ValueError(
                    "Patient not found"
                )

            history.patient_id = data["patient_id"]

        if "history_type" in data:
            history.history_type = data["history_type"]

        if "description" in data:
            history.description = data["description"]

        if "diagnosis_date" in data:
            history.diagnosis_date = (
                data["diagnosis_date"]
            )

        if "notes" in data:
            history.notes = data["notes"]

        return (
            PatientMedicalHistoryRepository.update(
                history
            )
        )

    @staticmethod
    def delete(history_id):
        history = (
            PatientMedicalHistoryService
            .get_by_id(history_id)
        )

        PatientMedicalHistoryRepository.delete(
            history
        )

        return True