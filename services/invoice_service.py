from datetime import date

from models.invoice import Invoice
from models.patient import Patient
from models.appointment import Appointment

from repositories.invoice_repository import InvoiceRepository


class InvoiceService:

    @staticmethod
    def create(data):
        # Check patient
        patient = Patient.query.get(
            data["patient_id"]
        )

        if not patient:
            raise ValueError("Patient not found")

        # Check appointment if provided
        appointment_id = data.get("appointment_id")

        if appointment_id is not None:
            appointment = Appointment.query.get(
                appointment_id
            )

            if not appointment:
                raise ValueError("Appointment not found")

        # Get financial values
        subtotal = data.get("subtotal", 0)
        tax = data.get("tax", 0)
        discount = data.get("discount", 0)

        # Validate amounts
        if subtotal < 0:
            raise ValueError(
                "Subtotal cannot be negative"
            )

        if tax < 0:
            raise ValueError(
                "Tax cannot be negative"
            )

        if discount < 0:
            raise ValueError(
                "Discount cannot be negative"
            )

        if discount > subtotal:
            raise ValueError(
                "Discount cannot be greater than subtotal"
            )

        # Calculate total
        total_amount = subtotal + tax - discount

        # Create invoice
        invoice = Invoice(
            invoice_number=data["invoice_number"],
            patient_id=data["patient_id"],
            appointment_id=appointment_id,
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            total_amount=total_amount,
            payment_status=data.get(
                "payment_status",
                "pending"
            ),
            due_date=data.get("due_date")
        )

        return InvoiceRepository.create(invoice)

    @staticmethod
    def get_by_id(invoice_id):
        invoice = InvoiceRepository.get_by_id(
            invoice_id
        )

        if not invoice:
            raise ValueError("Invoice not found")

        return invoice

    @staticmethod
    def get_all():
        return InvoiceRepository.get_all()

    @staticmethod
    def get_by_patient_id(patient_id):
        patient = Patient.query.get(patient_id)

        if not patient:
            raise ValueError("Patient not found")

        return InvoiceRepository.get_by_patient_id(
            patient_id
        )

    @staticmethod
    def update(invoice_id, data):
        invoice = InvoiceService.get_by_id(
            invoice_id
        )

        if "patient_id" in data:
            patient = Patient.query.get(
                data["patient_id"]
            )

            if not patient:
                raise ValueError(
                    "Patient not found"
                )

            invoice.patient_id = data["patient_id"]

        if "appointment_id" in data:
            appointment_id = data["appointment_id"]

            if appointment_id is not None:
                appointment = Appointment.query.get(
                    appointment_id
                )

                if not appointment:
                    raise ValueError(
                        "Appointment not found"
                    )

            invoice.appointment_id = appointment_id

        if "invoice_number" in data:
            invoice.invoice_number = (
                data["invoice_number"]
            )

        if "subtotal" in data:
            if data["subtotal"] < 0:
                raise ValueError(
                    "Subtotal cannot be negative"
                )

            invoice.subtotal = data["subtotal"]

        if "tax" in data:
            if data["tax"] < 0:
                raise ValueError(
                    "Tax cannot be negative"
                )

            invoice.tax = data["tax"]

        if "discount" in data:
            if data["discount"] < 0:
                raise ValueError(
                    "Discount cannot be negative"
                )

            invoice.discount = data["discount"]

        # Validate discount against subtotal
        if invoice.discount > invoice.subtotal:
            raise ValueError(
                "Discount cannot be greater than subtotal"
            )

        # Recalculate total
        invoice.total_amount = (
            invoice.subtotal
            + invoice.tax
            - invoice.discount
        )

        if "payment_status" in data:
            invoice.payment_status = (
                data["payment_status"]
            )

        if "due_date" in data:
            invoice.due_date = data["due_date"]

        return InvoiceRepository.update(invoice)

    @staticmethod
    def delete(invoice_id):
        invoice = InvoiceService.get_by_id(invoice_id)
        InvoiceRepository.delete(invoice)
        return True   
    