from flask import Blueprint
from flask_restful import Api

from resources.payment_resource import (
    PaymentListResource,
    PaymentResource,
    PaymentsByInvoiceResource
)


payment_bp = Blueprint(
    "payment",
    __name__,
    url_prefix="/api/v1/payments"
)

payment_api = Api(payment_bp)

payment_api.add_resource(
    PaymentListResource,
    ""
) 

payment_api.add_resource(
    PaymentResource,
    "/<int:payment_id>"
)

payment_api.add_resource(
    PaymentsByInvoiceResource,
    "/invoice/<int:invoice_id>"
)