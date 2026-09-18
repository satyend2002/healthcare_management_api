from models.medicine import Medicine
from repositories.medicine_repository import MedicineRepository


class MedicineService:

    @staticmethod
    def create(data):
        stock_quantity = data.get("stock_quantity", 0)
        reorder_level = data.get("reorder_level", 10)

        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")

        if reorder_level < 0:
            raise ValueError("Reorder level cannot be negative")

        medicine = Medicine(
            name=data["name"],
            generic_name=data.get("generic_name"),
            brand_name=data.get("brand_name"),
            strength=data.get("strength"),
            dosage_form=data.get("dosage_form"),
            manufacturer=data.get("manufacturer"),
            stock_quantity=stock_quantity,
            reorder_level=reorder_level,
            active=data.get("active", True)
        )

        return MedicineRepository.create(medicine)

    @staticmethod
    def get_by_id(medicine_id):
        medicine = MedicineRepository.get_by_id(medicine_id)

        if not medicine:
            raise ValueError("Medicine not found")

        return medicine


    @staticmethod
    def get_all(
        page=1,
        per_page=10,
        search="",
        active=None,
        low_stock=None,
        sort_by="id",
        order="asc"
    ):
        return MedicineRepository.get_all(
            page=page,
            per_page=per_page,
            search=search,
            active=active,
            low_stock=low_stock,
            sort_by=sort_by,
            order=order
        )


    @staticmethod
    def update(medicine_id, data):
        medicine = MedicineService.get_by_id(medicine_id)
        
        if "name" in data:
            medicine.name = data["name"]

        if "generic_name" in data:
            medicine.generic_name = data["generic_name"]

        if "brand_name" in data:
            medicine.brand_name = data["brand_name"]

        if "strength" in data:
            medicine.strength = data["strength"]

        if "dosage_form" in data:
            medicine.dosage_form = data["dosage_form"]

        if "manufacturer" in data:
            medicine.manufacturer = data["manufacturer"]

        if "stock_quantity" in data:
            if data["stock_quantity"] < 0:
                raise ValueError(
                    "Stock quantity cannot be negative"
                )

            medicine.stock_quantity = data["stock_quantity"]

        if "reorder_level" in data:
            if data["reorder_level"] < 0:
                raise ValueError(
                    "Reorder level cannot be negative"
                )

            medicine.reorder_level = data["reorder_level"]

        if "active" in data:
            medicine.active = data["active"]

        return MedicineRepository.update(medicine)


    @staticmethod
    def delete(medicine_id):
        medicine = MedicineService.get_by_id(medicine_id)
        MedicineRepository.delete(medicine)
        return True 