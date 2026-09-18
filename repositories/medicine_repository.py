from models.medicine import Medicine
from extensions.extensions import db
from sqlalchemy import or_


class MedicineRepository:

    @staticmethod
    def create(medicine):
        db.session.add(medicine)
        db.session.commit()
        return medicine

    @staticmethod
    def get_by_id(medicine_id):
        return Medicine.query.get(medicine_id)

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
        query = Medicine.query

        # Search by medicine, generic, or brand name
        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    Medicine.name.ilike(search_pattern),
                    Medicine.generic_name.ilike(search_pattern),
                    Medicine.brand_name.ilike(search_pattern)
                )
            )

        # Filter by active/inactive status
        if active is not None:
            active_value = active.lower()

            if active_value in ("true", "1", "yes"):
                query = query.filter(Medicine.active.is_(True))
            elif active_value in ("false", "0", "no"):
                query = query.filter(Medicine.active.is_(False))

        # Filter medicines whose stock is at or below reorder level
        if low_stock is not None:
            low_stock_value = low_stock.lower()

            if low_stock_value in ("true", "1", "yes"):
                query = query.filter(
                    Medicine.stock_quantity <= Medicine.reorder_level
                )

        # Allowed sorting fields
        allowed_sort_fields = {
            "id": Medicine.id,
            "name": Medicine.name,
            "stock_quantity": Medicine.stock_quantity,
            "reorder_level": Medicine.reorder_level,
            "created_at": Medicine.created_at
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Medicine.id
        )

        # Apply stable sorting
        if order == "desc":
            query = query.order_by(
                sort_column.desc(),
                Medicine.id.desc()
            )
        else:
            query = query.order_by(
                sort_column.asc(),
                Medicine.id.asc()
            )

        # Apply pagination
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def update(medicine):
        db.session.commit()
        return medicine

    @staticmethod
    def delete(medicine):
        db.session.delete(medicine)
        db.session.commit()