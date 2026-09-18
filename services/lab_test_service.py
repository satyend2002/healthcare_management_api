from models.lab_test import LabTest
from repositories.lab_test_repository import LabTestRepository


class LabTestService:

    @staticmethod
    def create(data):
        price = data.get("price", 0)

        if price < 0:
            raise ValueError("Price cannot be negative")

        lab_test = LabTest(
            test_code=data["test_code"],
            test_name=data["test_name"],
            description=data.get("description"),
            sample_type=data.get("sample_type"),
            price=price,
            active=data.get("active", True)
        )

        return LabTestRepository.create(lab_test)

    @staticmethod
    def get_by_id(lab_test_id):
        lab_test = LabTestRepository.get_by_id(lab_test_id)

        if not lab_test:
            raise ValueError("Laboratory test not found")

        return lab_test

    @staticmethod
    def get_all():
        return LabTestRepository.get_all()

    @staticmethod
    def update(lab_test_id, data):
        lab_test = LabTestService.get_by_id(lab_test_id)

        if "test_code" in data:
            lab_test.test_code = data["test_code"]

        if "test_name" in data:
            lab_test.test_name = data["test_name"]

        if "description" in data:
            lab_test.description = data["description"]

        if "sample_type" in data:
            lab_test.sample_type = data["sample_type"]

        if "price" in data:
            if data["price"] < 0:
                raise ValueError("Price cannot be negative")

            lab_test.price = data["price"]

        if "active" in data:
            lab_test.active = data["active"]

        return LabTestRepository.update(lab_test)

    @staticmethod
    def delete(lab_test_id):
        lab_test = LabTestService.get_by_id(lab_test_id)
        LabTestRepository.delete(lab_test)

        return True