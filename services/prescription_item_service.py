from models.prescription_item import PrescriptionItem
from models.prescription import Prescription
from models.medicine import Medicine

from repositories.prescription_item_repository import (
    PrescriptionItemRepository
)


class PrescriptionItemService:

    @staticmethod
    def create(data):
        prescription = Prescription.query.get(
            data["prescription_id"]
        )

        if not prescription:
            raise ValueError("Prescription not found")

        medicine = Medicine.query.get(
            data["medicine_id"]
        )

        if not medicine:
            raise ValueError("Medicine not found")

        if not medicine.active:
            raise ValueError("Medicine is inactive")

        prescription_item = PrescriptionItem(
            prescription_id=data["prescription_id"],
            medicine_id=data["medicine_id"],
            dosage=data["dosage"],
            frequency=data["frequency"],
            duration=data["duration"],
            instructions=data.get("instructions")
        )

        return PrescriptionItemRepository.create(
            prescription_item
        )

    @staticmethod
    def get_by_id(prescription_item_id):
        prescription_item = (
            PrescriptionItemRepository.get_by_id(
                prescription_item_id
            )
        )

        if not prescription_item:
            raise ValueError("Prescription item not found")

        return prescription_item

    @staticmethod
    def get_all():
        return PrescriptionItemRepository.get_all()

    @staticmethod
    def get_by_prescription_id(prescription_id):
        prescription = Prescription.query.get(
            prescription_id
        )

        if not prescription:
            raise ValueError("Prescription not found")

        return PrescriptionItemRepository.get_by_prescription_id(
            prescription_id
        )

    @staticmethod
    def update(prescription_item_id, data):
        prescription_item = (
            PrescriptionItemService.get_by_id(
                prescription_item_id
            )
        )

        if "prescription_id" in data:
            prescription = Prescription.query.get(
                data["prescription_id"]
            )

            if not prescription:
                raise ValueError("Prescription not found")

            prescription_item.prescription_id = (
                data["prescription_id"]
            )

        if "medicine_id" in data:
            medicine = Medicine.query.get(
                data["medicine_id"]
            )

            if not medicine:
                raise ValueError("Medicine not found")

            if not medicine.active:
                raise ValueError("Medicine is inactive")

            prescription_item.medicine_id = (
                data["medicine_id"]
            )

        if "dosage" in data:
            prescription_item.dosage = data["dosage"]

        if "frequency" in data:
            prescription_item.frequency = data["frequency"]

        if "duration" in data:
            prescription_item.duration = data["duration"]

        if "instructions" in data:
            prescription_item.instructions = data["instructions"]

        return PrescriptionItemRepository.update(
            prescription_item
        )

    @staticmethod
    def delete(prescription_item_id):
        prescription_item = (
            PrescriptionItemService.get_by_id(
                prescription_item_id
            )
        )

        PrescriptionItemRepository.delete(
            prescription_item
        )

        return True