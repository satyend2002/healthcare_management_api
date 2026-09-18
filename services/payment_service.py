from models.payment import Payment
from models.invoice import Invoice
from repositories.payment_repository import PaymentRepository


class PaymentService:

    @staticmethod
    def create(data):
        invoice = Invoice.query.get(data["invoice_id"])

        if not invoice:
            raise ValueError("Invoice not found")

        amount = data["amount"]

        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        payment = Payment(
            payment_reference=data["payment_reference"],
            invoice_id=data["invoice_id"],
            amount=amount,
            payment_method=data["payment_method"],
            payment_date=data.get("payment_date"),
            status=data.get("status", "completed"),
            notes=data.get("notes")
        )

        return PaymentRepository.create(payment)


    @staticmethod
    def get_by_id(payment_id):
        payment = PaymentRepository.get_by_id(payment_id)

        if not payment:
            raise ValueError("Payment not found")

        return payment


    @staticmethod
    def get_all():
        return PaymentRepository.get_all()


    @staticmethod
    def get_by_invoice_id(invoice_id):
        invoice = Invoice.query.get(invoice_id)

        if not invoice:
            raise ValueError("Invoice not found")

        return PaymentRepository.get_by_invoice_id(invoice_id)


    @staticmethod
    def update(payment_id, data):
        payment = PaymentService.get_by_id(payment_id)

        if "invoice_id" in data:
            invoice = Invoice.query.get(data["invoice_id"])

            if not invoice:
                raise ValueError("Invoice not found")

            payment.invoice_id = data["invoice_id"]

        if "payment_reference" in data:
            payment.payment_reference = data["payment_reference"]

        if "amount" in data:
            if data["amount"] <= 0:
                raise ValueError("Payment amount must be greater than zero")

            payment.amount = data["amount"]

        if "payment_method" in data:
            payment.payment_method = data["payment_method"]

        if "payment_date" in data:
            payment.payment_date = data["payment_date"]

        if "status" in data:
            payment.status = data["status"]

        if "notes" in data:
            payment.notes = data["notes"]

        return PaymentRepository.update(payment)



    @staticmethod
    def delete(payment_id):
        payment = PaymentService.get_by_id(payment_id)
        PaymentRepository.delete(payment)

        return True