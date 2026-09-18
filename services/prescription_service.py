from models.prescription import Prescription
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

from repositories.prescription_repository import PrescriptionRepository


class PrescriptionService:

    @staticmethod
    def create(data):
        # Check patient
        patient = Patient.query.get(data["patient_id"])

        if not patient:
            raise ValueError("Patient not found")

        # Check doctor
        doctor = Doctor.query.get(data["doctor_id"])

        if not doctor:
            raise ValueError("Doctor not found")

        # Check appointment
        appointment = Appointment.query.get(data["appointment_id"])

        if not appointment:
            raise ValueError("Appointment not found")

        # Create prescription
        prescription = Prescription(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            appointment_id=data["appointment_id"],
            medicine_name=data["medicine_name"],
            dosage=data["dosage"],
            frequency=data["frequency"],
            duration=data["duration"],
            instructions=data.get("instructions")
        )

        return PrescriptionRepository.create(prescription)

    @staticmethod
    def get_by_id(prescription_id):
        prescription = PrescriptionRepository.get_by_id(
            prescription_id
        )

        if not prescription:
            raise ValueError("Prescription not found")

        return prescription

    @staticmethod
    def get_all(page=1, per_page=10):
        return PrescriptionRepository.get_all(
            page=page,
            per_page=per_page
        )

    @staticmethod
    def update(prescription_id, data):
        prescription = PrescriptionService.get_by_id(
            prescription_id
        )

        if "patient_id" in data:
            patient = Patient.query.get(data["patient_id"])

            if not patient:
                raise ValueError("Patient not found")

            prescription.patient_id = data["patient_id"]

        if "doctor_id" in data:
            doctor = Doctor.query.get(data["doctor_id"])

            if not doctor:
                raise ValueError("Doctor not found")

            prescription.doctor_id = data["doctor_id"]

        if "appointment_id" in data:
            appointment = Appointment.query.get(
                data["appointment_id"]
            )

            if not appointment:
                raise ValueError("Appointment not found")

            prescription.appointment_id = data["appointment_id"]
            

        if "medicine_name" in data:
            prescription.medicine_name = data["medicine_name"]

        if "dosage" in data:
            prescription.dosage = data["dosage"]

        if "frequency" in data:
            prescription.frequency = data["frequency"]

        if "duration" in data:
            prescription.duration = data["duration"]

        if "instructions" in data:
            prescription.instructions = data["instructions"]

        return PrescriptionRepository.update(prescription)

    @staticmethod
    def delete(prescription_id):
        prescription = PrescriptionService.get_by_id(
            prescription_id
        )

        PrescriptionRepository.delete(prescription)

        return True