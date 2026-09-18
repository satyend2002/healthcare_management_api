from flask import Blueprint
from flask_restful import Api

from resources.invoice_resource import (
    InvoiceListResource,
    InvoiceResource,
    InvoicesByPatientResource
)


invoice_bp = Blueprint(
    "invoice",
    __name__,
    url_prefix="/api/v1/invoices"
)

invoice_api = Api(invoice_bp)


invoice_api.add_resource(
    InvoiceListResource,
    ""
)

invoice_api.add_resource(
    InvoiceResource,
    "/<int:invoice_id>"
)

invoice_api.add_resource(
    InvoicesByPatientResource,
    "/patient/<int:patient_id>"
)